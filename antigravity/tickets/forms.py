from django import forms


class CheckoutForm(forms.Form):
    nombre_titular = forms.CharField(
        label='Nombre en la tarjeta',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'JUAN PEREZ', 'autocomplete': 'cc-name'}),
    )
    numero_tarjeta = forms.CharField(
        label='Número de tarjeta',
        max_length=19,
        widget=forms.TextInput(
            attrs={
                'placeholder': '1234 5678 9012 3456',
                'autocomplete': 'cc-number',
                'maxlength': '19',
                'inputmode': 'numeric',
            }
        ),
    )
    expiracion = forms.CharField(
        label='Fecha de expiración',
        max_length=5,
        widget=forms.TextInput(
            attrs={'placeholder': 'MM/AA', 'autocomplete': 'cc-exp', 'maxlength': '5'}
        ),
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=4,
        widget=forms.TextInput(
            attrs={'placeholder': '123', 'autocomplete': 'cc-csc', 'maxlength': '4', 'inputmode': 'numeric'}
        ),
    )
    cantidad = forms.IntegerField(
        label='Cantidad de entradas',
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'min': '1', 'max': '10'}),
    )

    def clean_numero_tarjeta(self):
        numero = self.cleaned_data['numero_tarjeta'].replace(' ', '').replace('-', '')
        if not numero.isdigit():
            raise forms.ValidationError('El número de tarjeta solo debe contener dígitos.')
        if len(numero) < 13 or len(numero) > 16:
            raise forms.ValidationError('El número de tarjeta debe tener entre 13 y 16 dígitos.')
        return numero

    def clean_expiracion(self):
        exp = self.cleaned_data['expiracion']
        if '/' not in exp or len(exp) != 5:
            raise forms.ValidationError('Formato inválido. Usa MM/AA.')
        return exp

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit():
            raise forms.ValidationError('El CVV solo debe contener dígitos.')
        return cvv


class ValidarEntradaForm(forms.Form):
    codigo = forms.UUIDField(
        label='Código UUID de la entrada',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                'autocomplete': 'off',
            }
        ),
    )
