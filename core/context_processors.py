"""
Custom context processors used across Bela Crochet templates.

These functions provide site‑wide settings and mini‑cart summaries so
that templates can easily access the brand information and the number
of items currently in a visitor's cart.
"""
from __future__ import annotations

from django.conf import settings
from django.db.models import Sum, F

from .models import SiteSetting
from cart.models import Cart, CartItem


def site_settings(request):
    """Injects global site settings into the context."""
    try:
        setting = SiteSetting.objects.first()
    except Exception:
        setting = None
    return {
        "site_settings": setting,
        "brand_name": setting.brand_name if setting else "Bela Crochet",
    }


def cart_mini(request):
    """Return a mini cart summary: total quantity and total price."""
    total_qty = 0
    total_price = 0
    # Determine the cart: logged in user or session
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.get(settings.CART_SESSION_ID)
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
    if cart:
        total_qty = cart.items.aggregate(total=Sum("quantity"))[("total")] or 0
        total_price = sum(item.line_subtotal() for item in cart.items.all())
    return {
        "cart_total_qty": total_qty or 0,
        "cart_total_price": total_price or 0,
    }