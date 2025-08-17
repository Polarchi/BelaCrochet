"""
Models for the core app.

These models provide central functionality that other apps can reuse.
"""
from __future__ import annotations

from django.db import models


class MediaImage(models.Model):
    """Reusable image stored in the media library."""
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to="media_images/")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Media image"
        verbose_name_plural = "Media images"

    def __str__(self) -> str:
        return self.name


class SiteSetting(models.Model):
    """
    Stores global site preferences such as brand name, logo, and palette.
    Only one instance is expected.
    """
    brand_name = models.CharField(max_length=120, default="Bela Crochet")
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    palette_primary = models.CharField(
        max_length=7, default="#f5e9e5", help_text="Primary brand colour"
    )
    palette_secondary = models.CharField(
        max_length=7, default="#caa6c7", help_text="Secondary brand colour"
    )
    palette_accent = models.CharField(
        max_length=7, default="#e3d4e6", help_text="Accent colour"
    )
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site setting"
        verbose_name_plural = "Site settings"

    def __str__(self) -> str:
        return self.brand_name