"""
Checkout view to collect shipping information, create an order and redirect to the receipt.
"""
from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from cart.models import Cart, CartItem
from cart.views import _get_cart
from orders.models import Order, OrderItem
from receipts.models import Receipt
from .forms import ShippingForm


class CheckoutView(View):
    template_name = "checkout/checkout.html"

    def get(self, request):
        cart = _get_cart(request)
        if not cart or not cart.items.exists():
            return redirect("cart:cart_detail")
        form = ShippingForm()
        return render(
            request,
            self.template_name,
            {"form": form, "cart": cart, "items": cart.items, "total": cart.total_price()},
        )

    def post(self, request):
        cart = _get_cart(request)
        form = ShippingForm(request.POST)
        if not cart or not cart.items.exists():
            return redirect("cart:cart_detail")
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                status="confirmado",
                shipping_full_name=data["full_name"],
                shipping_address_line1=data["line1"],
                shipping_address_line2=data.get("line2", ""),
                shipping_city=data["city"],
                shipping_state=data.get("state", ""),
                shipping_postal_code=data.get("postal_code", ""),
                shipping_country=data.get("country", "Ecuador"),
            )
            # Create order items
            for item in cart.items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product_name=item.variant.product.name,
                    variant_name=item.variant.name,
                    sku=item.variant.sku,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                    line_total=item.unit_price * item.quantity,
                )
                # decrease inventory
                if hasattr(item.variant, "inventory"):
                    inv = item.variant.inventory
                    if inv.quantity >= item.quantity:
                        inv.quantity -= item.quantity
                        inv.save()
            # calculate totals
            order.calculate_totals()
            # create receipt
            receipt = Receipt.objects.create(order=order)
            # clear cart
            cart.items.all().delete()
            cart.delete()
            # remove session key for anonymous users
            if not request.user.is_authenticated:
                request.session.pop(settings.CART_SESSION_ID, None)
            return redirect("receipts:receipt_detail", order_number=order.order_number)
        return render(
            request,
            self.template_name,
            {"form": form, "cart": cart, "items": cart.items, "total": cart.total_price()},
        )