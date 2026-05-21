from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import EventoForm, PrecioCategoriaFormSet, UbicacionForm
from .models import Evento, PrecioCategoria, Ubicacion


class HomeView(View):
    def get(self, request):
        eventos = Evento.objects.filter(estado=Evento.PUBLICADO).select_related('ubicacion', 'organizador')[:6]
        return render(request, 'home.html', {'eventos': eventos})


class EventListView(ListView):
    model = Evento
    template_name = 'events/list.html'
    context_object_name = 'eventos'
    paginate_by = 9

    def get_queryset(self):
        qs = Evento.objects.filter(estado=Evento.PUBLICADO).select_related('ubicacion', 'organizador')
        q = self.request.GET.get('q')
        ciudad = self.request.GET.get('ciudad')
        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(descripcion__icontains=q))
        if ciudad:
            qs = qs.filter(ubicacion__ciudad__icontains=ciudad)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['ciudades'] = (
            Ubicacion.objects.filter(eventos__estado=Evento.PUBLICADO)
            .values_list('ciudad', flat=True)
            .distinct()
        )
        ctx['q'] = self.request.GET.get('q', '')
        ctx['ciudad_sel'] = self.request.GET.get('ciudad', '')
        return ctx


class EventDetailView(DetailView):
    model = Evento
    template_name = 'events/detail.html'
    context_object_name = 'evento'

    def get_queryset(self):
        qs = Evento.objects.filter(estado=Evento.PUBLICADO)
        if self.request.user.is_authenticated and self.request.user.is_organizador:
            qs = (qs | Evento.objects.filter(organizador=self.request.user)).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categorias'] = self.object.categorias.all()
        return ctx


class OrganizerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_organizador


class EventManageView(OrganizerRequiredMixin, View):
    template_name = 'events/manage.html'

    def get(self, request):
        eventos = Evento.objects.filter(organizador=request.user).select_related('ubicacion')
        return render(request, self.template_name, {'eventos': eventos})


class EventCreateView(OrganizerRequiredMixin, View):
    template_name = 'events/form.html'

    def get(self, request):
        form = EventoForm()
        formset = PrecioCategoriaFormSet()
        ubicacion_form = UbicacionForm()
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'ubicacion_form': ubicacion_form,
            'title': 'Crear Evento',
        })

    def post(self, request):
        form = EventoForm(request.POST, request.FILES)
        formset = PrecioCategoriaFormSet(request.POST)
        ubicacion_form = UbicacionForm(request.POST)

        if form.is_valid() and formset.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.save()
            formset.instance = evento
            formset.save()
            messages.success(request, f'Evento "{evento.titulo}" creado correctamente.')
            return redirect('events:manage')

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'ubicacion_form': ubicacion_form,
            'title': 'Crear Evento',
        })


class EventUpdateView(OrganizerRequiredMixin, View):
    template_name = 'events/form.html'

    def _get_evento(self, request, pk):
        return get_object_or_404(Evento, pk=pk, organizador=request.user)

    def get(self, request, pk):
        evento = self._get_evento(request, pk)
        form = EventoForm(instance=evento)
        formset = PrecioCategoriaFormSet(instance=evento)
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'evento': evento,
            'title': f'Editar: {evento.titulo}',
        })

    def post(self, request, pk):
        evento = self._get_evento(request, pk)
        form = EventoForm(request.POST, request.FILES, instance=evento)
        formset = PrecioCategoriaFormSet(request.POST, instance=evento)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'Evento "{evento.titulo}" actualizado.')
            return redirect('events:manage')

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'evento': evento,
            'title': f'Editar: {evento.titulo}',
        })


class EventDeleteView(OrganizerRequiredMixin, View):
    def post(self, request, pk):
        evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
        titulo = evento.titulo
        evento.delete()
        messages.success(request, f'Evento "{titulo}" eliminado.')
        return redirect('events:manage')
