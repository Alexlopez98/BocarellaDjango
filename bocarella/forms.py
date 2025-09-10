from django import forms
from django.contrib.auth.models import User
from .models import Perfil
import re

class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Confirmar contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,18}$'
        if not re.match(regex, password):
            raise forms.ValidationError(
                "La contraseña debe tener 6-18 caracteres, al menos una mayúscula, un número y un carácter especial (@$!%*?&)."
            )
        return password

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('password_confirm')
        if password and confirm and password != confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden")
        return cleaned


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['direccion']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
