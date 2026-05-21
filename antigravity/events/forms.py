from django import forms
from django.forms import inlineformset_factory
from .models import Evento, Ubicacion, PrecioCategoria


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ('nombre', 'direccion', 'ciudad', 'capacidad_maxima')
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Centro de Convenciones Ágora'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Carrera 37 # 24-67'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Bogotá'}),
            'capacidad_maxima': forms.NumberInput(attrs={'placeholder': '500', 'min': '1'}),
        }


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ('titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'imagen_banner', 'estado', 'ubicacion')
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Nombre del evento'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe el evento…'}),
            'fecha_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'estado': forms.Select(),
            'ubicacion': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['imagen_banner'].required = False


PrecioCategoriaFormSet = inlineformset_factory(
    Evento,
    PrecioCategoria,
    fields=('nombre', 'precio', 'cantidad_disponible'),
    widgets={
        'nombre': forms.TextInput(attrs={'placeholder': 'Ej. General, VIP…'}),
        'precio': forms.NumberInput(attrs={'placeholder': '0.00', 'min': '0', 'step': '0.01'}),
        'cantidad_disponible': forms.NumberInput(attrs={'placeholder': '100', 'min': '1'}),
    },
    extra=2,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
