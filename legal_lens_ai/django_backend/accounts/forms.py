from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LawyerRegisterForm(UserCreationForm):
    """Formulario de registro de abogados."""

    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellidos")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
