"""
Models for orders and order items.
"""
from __future__ import annotations

import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models, IntegrityError
from django.utils import timezone


def generate_order_number() -> str:
    """Generate an order number like BC-YYYYMMDD-XXXXXX (único)."""
    date_part = timezone.localdate().strftime("%Y%m%d")
    # sufijo aleatorio corto para evitar colisiones en concurrencia
    suffix = uuid.uuid4().hex[:6].upper()
    return f"BC-{date_part}-{suffix}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("creado", "Creado"),
        ("confirmado", "Confirmado"),
        ("preparacion", "En preparación"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    # importante: generar por defecto y no editable
    order_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        default=generate_order_number,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="creado")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # shipping info snapshot
    shipping_full_name = models.CharField(max_length=100)
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True)
    shipping_country = models.CharField(max_length=100, default="Ecuador")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.order_number

    def save(self, *args, **kwargs):
        # Garantiza un valor y reintenta si hubiese colisión por unique
        if not self.order_number:
            self.order_number = generate_order_number()

        for _ in range(5):
            try:
                return super().save(*args, **kwargs)
            except IntegrityError as e:
                # si choca la restricción única, generamos otro y reintentamos
                if "orders_order.order_number" in str(e):
                    self.order_number = generate_order_number()
                    continue
                raise
        # si algo raro pasa repetidamente, propagamos el error
        raise

    def calculate_totals(self):
        subtotal = sum((item.line_total for item in self.items.all()), Decimal("0.00"))
        self.subtotal = subtotal
        self.shipping_cost = Decimal("0.00")
        self.total = self.subtotal + self.shipping_cost - self.discount_total
        self.save(update_fields=["subtotal", "shipping_cost", "total"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=150)
    variant_name = models.CharField(max_length=50)
    sku = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Línea de pedido"
        verbose_name_plural = "Líneas de pedido"

    def __str__(self) -> str:
        return f"{self.product_name} - {self.variant_name} (x{self.quantity})"
