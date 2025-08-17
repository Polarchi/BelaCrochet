"""
Models for simple static pages editable from the admin.
"""
from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SimplePage(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=150)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("pages:detail", args=[self.slug])