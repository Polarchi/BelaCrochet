"""
Views for cart operations: view cart, add items, update and remove.
"""
from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from catalog.models import Product, Variant
from .models import Cart, CartItem


def _get_cart(request) -> Cart:
    """Helper to fetch or create a cart for the current user or session."""
    cart = None
    if request.user.is_authenticated:
        cart, _created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.get(settings.CART_SESSION_ID)
        if not session_key:
            # create a new session cart
            request.session[settings.CART_SESSION_ID] = request.session.session_key or request.session._get_or_create_session_key()
            session_key = request.session[settings.CART_SESSION_ID]
        cart, _created = Cart.objects.get_or_create(session_key=session_key)
    return cart


class AddToCartView(View):
    def post(self, request, product_slug):
        variant_id = request.POST.get("variant_id")
        quantity = int(request.POST.get("quantity", 1))
        variant = get_object_or_404(Variant, id=variant_id)
        cart = _get_cart(request)
        # Add or update item
        item, created = CartItem.objects.get_or_create(cart=cart, variant=variant, defaults={"unit_price": variant.display_price})
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.unit_price = variant.display_price  # snapshot
        item.save()
        return redirect("cart:cart_detail")


class CartDetailView(TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = _get_cart(self.request)
        context["cart"] = cart
        context["items"] = cart.items
        context["total_price"] = cart.total_price() if cart else Decimal("0.00")
        return context


class UpdateCartItemView(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        return redirect("cart:cart_detail")


class RemoveCartItemView(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        return redirect("cart:cart_detail")