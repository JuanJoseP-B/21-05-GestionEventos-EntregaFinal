from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ORGANIZADOR = 'ORGANIZADOR'
    ASISTENTE = 'ASISTENTE'
    OPERADOR = 'OPERADOR'

    ROL_CHOICES = [
        (ORGANIZADOR, 'Organizador'),
        (ASISTENTE, 'Asistente'),
        (OPERADOR, 'Operador'),
    ]

    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default=ASISTENTE)
    telefono = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_rol_display()})'

    @property
    def is_organizador(self):
        return self.rol == self.ORGANIZADOR

    @property
    def is_asistente(self):
        return self.rol == self.ASISTENTE

    @property
    def is_operador(self):
        return self.rol == self.OPERADOR
