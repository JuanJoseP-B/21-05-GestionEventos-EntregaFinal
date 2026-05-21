import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from events.models import Evento, PrecioCategoria
from .forms import CheckoutForm, ValidarEntradaForm
from .models import Entrada


class AsistenteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_asistente


class OrganizerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_organizador


class OperadorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_operador or self.request.user.is_organizador


class CheckoutView(AsistenteRequiredMixin, View):
    template_name = 'tickets/checkout.html'

    def _get_categoria(self, pk):
        return get_object_or_404(
            PrecioCategoria.objects.select_related('evento'),
            pk=pk,
            evento__estado=Evento.PUBLICADO,
        )

    def get(self, request, categoria_pk):
        categoria = self._get_categoria(categoria_pk)
        if categoria.agotado:
            messages.error(request, 'Esta categoría está agotada.')
            return redirect('events:detail', pk=categoria.evento.pk)
        form = CheckoutForm()
        return render(request, self.template_name, {'categoria': categoria, 'form': form})

    def post(self, request, categoria_pk):
        categoria = self._get_categoria(categoria_pk)
        form = CheckoutForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'categoria': categoria, 'form': form})

        cantidad = form.cleaned_data['cantidad']
        numero_tarjeta = form.cleaned_data['numero_tarjeta']

        if categoria.disponibles < cantidad:
            messages.error(request, f'Solo quedan {categoria.disponibles} entradas disponibles.')
            return render(request, self.template_name, {'categoria': categoria, 'form': form})

        # Simular delay de pasarela de pagos
        time.sleep(1)

        # Tarjetas que terminan en 9999 = rechazo simulado
        if numero_tarjeta.endswith('9999'):
            messages.error(request, 'Pago rechazado. Verifica los datos de tu tarjeta e intenta nuevamente.')
            return render(request, self.template_name, {'categoria': categoria, 'form': form})

        # Pago aprobado — crear entradas con transaction atómica
        entradas_creadas = []
        with transaction.atomic():
            for _ in range(cantidad):
                entrada = Entrada(
                    evento=categoria.evento,
                    asistente=request.user,
                    categoria=categoria,
                    pagado=True,
                )
                entrada.generar_qr(request)
                entrada.save()
                entradas_creadas.append(entrada)

        # Enviar correo de confirmación (consola en dev, SMTP en producción)
        self._enviar_confirmacion(request.user, categoria.evento, entradas_creadas)

        messages.success(
            request,
            f'¡Compra exitosa! {cantidad} entrada(s) para {categoria.evento.titulo} generadas.',
        )
        if cantidad == 1:
            return redirect('tickets:detail', codigo=entradas_creadas[0].codigo_unico)
        return redirect('tickets:my_tickets')

    def _enviar_confirmacion(self, user, evento, entradas):
        codigos = '\n'.join(f'  • {e.codigo_unico}' for e in entradas)
        send_mail(
            subject=f'¡Tu entrada para {evento.titulo}!',
            message=(
                f'Hola {user.first_name or user.username},\n\n'
                f'Tu compra ha sido confirmada.\n'
                f'Evento: {evento.titulo}\n'
                f'Fecha: {evento.fecha_inicio.strftime("%d/%m/%Y %H:%M")}\n'
                f'Lugar: {evento.ubicacion}\n\n'
                f'Códigos de entrada:\n{codigos}\n\n'
                f'Descarga tus QRs desde la plataforma.\n\n— Antigravity'
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True,
        )


class MyTicketsView(LoginRequiredMixin, View):
    template_name = 'tickets/my_tickets.html'

    def get(self, request):
        entradas = (
            Entrada.objects.filter(asistente=request.user, pagado=True)
            .select_related('evento', 'categoria', 'evento__ubicacion')
            .order_by('-fecha_compra')
        )
        return render(request, self.template_name, {'entradas': entradas})


class TicketDetailView(LoginRequiredMixin, View):
    template_name = 'tickets/ticket_detail.html'

    def get(self, request, codigo):
        entrada = get_object_or_404(Entrada, codigo_unico=codigo)
        # Solo el asistente dueño o el organizador del evento pueden verla
        if entrada.asistente != request.user and entrada.evento.organizador != request.user:
            messages.error(request, 'No tienes permiso para ver esta entrada.')
            return redirect('home')
        return render(request, self.template_name, {'entrada': entrada})


class ValidarQRView(View):
    """Endpoint al que apunta el QR — valida y muestra resultado en HTML."""
    template_name = 'tickets/validate.html'

    def get(self, request, codigo):
        entrada = get_object_or_404(Entrada, codigo_unico=codigo)
        context = {'entrada': entrada, 'modo': 'qr'}

        if not entrada.pagado:
            context.update({'status': 'error', 'mensaje': 'Esta entrada no ha sido pagada.'})
        elif entrada.usado:
            context.update({
                'status': 'ya_usado',
                'mensaje': f'Entrada ya utilizada el {entrada.fecha_uso.strftime("%d/%m/%Y a las %H:%M")}.',
            })
        else:
            entrada.usado = True
            entrada.fecha_uso = timezone.now()
            entrada.save(update_fields=['usado', 'fecha_uso'])
            context.update({'status': 'success', 'mensaje': '¡Acceso Permitido! Bienvenido al evento.'})

        return render(request, self.template_name, context)


class CheckInView(OperadorRequiredMixin, View):
    """Panel de check-in para operadores — validación AJAX en tiempo real."""
    template_name = 'tickets/checkin.html'

    def get(self, request):
        form = ValidarEntradaForm()
        return render(request, self.template_name, {'form': form})


class ApiValidarView(OperadorRequiredMixin, View):
    """Endpoint AJAX que retorna JSON con el resultado de la validación."""

    def post(self, request):
        import json
        try:
            body = json.loads(request.body)
            codigo = body.get('codigo', '').strip()
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'status': 'error', 'mensaje': 'Solicitud inválida.'}, status=400)

        try:
            entrada = Entrada.objects.select_related('evento', 'asistente', 'categoria').get(
                codigo_unico=codigo
            )
        except (Entrada.DoesNotExist, ValueError):
            return JsonResponse({'status': 'not_found', 'mensaje': 'Entrada no encontrada.'})

        if not entrada.pagado:
            return JsonResponse({'status': 'error', 'mensaje': 'Entrada no pagada.'})

        if entrada.usado:
            return JsonResponse({
                'status': 'ya_usado',
                'mensaje': f'Entrada ya utilizada el {entrada.fecha_uso.strftime("%d/%m/%Y %H:%M")}.',
                'asistente': entrada.asistente.get_full_name() or entrada.asistente.username,
                'evento': entrada.evento.titulo,
                'categoria': entrada.categoria.nombre,
            })

        entrada.usado = True
        entrada.fecha_uso = timezone.now()
        entrada.save(update_fields=['usado', 'fecha_uso'])

        return JsonResponse({
            'status': 'success',
            'mensaje': '¡Acceso Permitido!',
            'asistente': entrada.asistente.get_full_name() or entrada.asistente.username,
            'evento': entrada.evento.titulo,
            'categoria': entrada.categoria.nombre,
        })


# ── Dashboard ──────────────────────────────────────────────────────────────

class DashboardView(OrganizerRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        eventos = Evento.objects.filter(organizador=request.user).prefetch_related('categorias', 'entradas')
        total_vendidas = sum(e.entradas_vendidas for e in eventos)
        total_ingresos = sum(e.ingresos_totales for e in eventos)
        return render(request, self.template_name, {
            'eventos': eventos,
            'total_vendidas': total_vendidas,
            'total_ingresos': total_ingresos,
        })


class ApiVentasCategoriaView(OrganizerRequiredMixin, View):
    def get(self, request, evento_id):
        evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
        categorias = PrecioCategoria.objects.filter(evento=evento)
        data = {
            'labels': [c.nombre for c in categorias],
            'vendidas': [c.vendidas for c in categorias],
            'ingresos': [float(c.vendidas * c.precio) for c in categorias],
            'disponibles': [c.disponibles for c in categorias],
        }
        return JsonResponse(data)


class ApiAsistenciaDiaView(OrganizerRequiredMixin, View):
    def get(self, request, evento_id):
        evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
        datos = (
            Entrada.objects.filter(evento=evento, pagado=True)
            .annotate(dia=TruncDate('fecha_compra'))
            .values('dia')
            .annotate(total=Count('id'))
            .order_by('dia')
        )
        return JsonResponse({
            'labels': [str(d['dia']) for d in datos],
            'counts': [d['total'] for d in datos],
        })


class ExportExcelView(OrganizerRequiredMixin, View):
    def get(self, request, evento_id):
        import pandas as pd
        evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
        entradas = (
            Entrada.objects.filter(evento=evento, pagado=True)
            .select_related('asistente', 'categoria')
            .order_by('fecha_compra')
        )
        data = [
            {
                'Código': str(e.codigo_unico),
                'Nombre': e.asistente.get_full_name() or e.asistente.username,
                'Correo': e.asistente.email,
                'Teléfono': e.asistente.telefono or '—',
                'Categoría': e.categoria.nombre,
                'Precio (COP)': float(e.categoria.precio),
                'Fecha Compra': e.fecha_compra.strftime('%Y-%m-%d %H:%M'),
                'Usado': 'Sí' if e.usado else 'No',
                'Fecha Uso': e.fecha_uso.strftime('%Y-%m-%d %H:%M') if e.fecha_uso else '—',
            }
            for e in entradas
        ]
        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        safe_title = ''.join(c for c in evento.titulo if c.isalnum() or c in (' ', '_')).rstrip()
        response['Content-Disposition'] = f'attachment; filename="asistentes_{safe_title}.xlsx"'
        df.to_excel(response, index=False, engine='openpyxl')
        return response
