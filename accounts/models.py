"""
User profiles, addresses and preferences.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extend the default Django User with additional attributes."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    language = models.CharField(max_length=10, default="es-ec")
    receive_newsletter = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Perfil de {self.user.username}"


class Address(models.Model):
    """Represents a shipping or billing address for a user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=100)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="Ecuador")
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.line1}, {self.city}"