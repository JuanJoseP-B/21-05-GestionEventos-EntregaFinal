import uuid

import qrcode
from django.conf import settings
from django.core.files import File
from django.db import models
from django.urls import reverse
from io import BytesIO


class Entrada(models.Model):
    codigo_unico = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    evento = models.ForeignKey(
        'events.Evento', on_delete=models.PROTECT, related_name='entradas'
    )
    asistente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'ASISTENTE'},
        related_name='entradas_compradas',
    )
    categoria = models.ForeignKey(
        'events.PrecioCategoria', on_delete=models.PROTECT, related_name='entradas'
    )
    pagado = models.BooleanField(default=False)
    usado = models.BooleanField(default=False)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    codigo_qr = models.ImageField(upload_to='tickets/qrs/', blank=True, null=True)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['-fecha_compra']

    def __str__(self):
        return f'Entrada {str(self.codigo_unico)[:8]}… — {self.evento.titulo}'

    def get_absolute_url(self):
        return reverse('tickets:detail', kwargs={'codigo': self.codigo_unico})

    def generar_qr(self, request=None):
        url = reverse('tickets:validar_qr', kwargs={'codigo': self.codigo_unico})
        if request:
            url = request.build_absolute_uri(url)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_{self.codigo_unico}.png'
        self.codigo_qr.save(filename, File(buffer), save=False)
