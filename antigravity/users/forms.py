from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario o correo',
        widget=forms.TextInput(attrs={'placeholder': 'Tu usuario', 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'current-password'}),
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=50)
    last_name = forms.CharField(label='Apellido', max_length=50)
    email = forms.EmailField(label='Correo electrónico')
    telefono = forms.CharField(label='Teléfono', max_length=20, required=False)
    rol = forms.ChoiceField(
        label='Registrarme como',
        choices=[
            (CustomUser.ASISTENTE, 'Asistente — quiero comprar entradas'),
            (CustomUser.ORGANIZADOR, 'Organizador — quiero crear eventos'),
        ],
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'rol', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Nombre de usuario',
            'first_name': 'Tu nombre',
            'last_name': 'Tu apellido',
            'email': 'correo@ejemplo.com',
            'telefono': '+57 300 000 0000',
            'password1': '••••••••',
            'password2': '••••••••',
        }
        for field, placeholder in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = placeholder


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'telefono')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+57 300 000 0000'}),
        }
