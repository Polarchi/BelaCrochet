"""
Models for storing order receipts.
"""
from __future__ import annotations

from django.db import models

from orders.models import Order


class Receipt(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="receipt")
    html_snapshot = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to="receipts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comprobante"
        verbose_name_plural = "Comprobantes"

    def __str__(self) -> str:
        return f"Recibo de {self.order.order_number}"