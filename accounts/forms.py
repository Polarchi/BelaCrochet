"""
Forms for user registration and address management.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Address, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text="Requerido. Ingresa un email válido.")
    receive_newsletter = forms.BooleanField(
        required=False, label="Deseo recibir novedades y promociones"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # create profile
            Profile.objects.create(
                user=user,
                receive_newsletter=self.cleaned_data.get("receive_newsletter", False),
            )
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        ]
        widgets = {
            "is_default": forms.CheckboxInput(),
        }