"""
Forms used during the checkout process.
"""
from django import forms


class ShippingForm(forms.Form):
    full_name = forms.CharField(label="Nombre completo", max_length=100)
    line1 = forms.CharField(label="Dirección", max_length=255)
    line2 = forms.CharField(label="Dirección 2", max_length=255, required=False)
    city = forms.CharField(label="Ciudad", max_length=100)
    state = forms.CharField(label="Provincia/Estado", max_length=100, required=False)
    postal_code = forms.CharField(label="Código postal", max_length=20, required=False)
    country = forms.CharField(label="País", max_length=100, initial="Ecuador")