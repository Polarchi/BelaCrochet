"""
Models representing shopping carts and their items.
"""
from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from catalog.models import Variant


class Cart(models.Model):
    """A shopping cart tied to a user or an anonymous session."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True,
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self) -> str:
        if self.user:
            return f"Carrito de {self.user.username}"
        return f"Carrito de sesión {self.session_key}"

    @property
    def items(self):
        return self.cartitem_set.all()

    def total_quantity(self) -> int:
        return sum(item.quantity for item in self.items)

    def total_price(self) -> Decimal:
        return sum(item.line_subtotal() for item in self.items)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Elemento del carrito"
        verbose_name_plural = "Elementos del carrito"
        unique_together = ("cart", "variant")

    def __str__(self) -> str:
        return f"{self.variant} (x{self.quantity})"

    def line_subtotal(self) -> Decimal:
        return self.unit_price * self.quantity

    @property
    def line_subtotal_prop(self) -> Decimal:
        """Return the subtotal for template usage."""
        return self.unit_price * self.quantity