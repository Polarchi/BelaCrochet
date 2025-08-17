"""
Views for displaying order receipts.
"""
from __future__ import annotations

from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.template.loader import render_to_string

from orders.models import Order
from .models import Receipt


class ReceiptDetailView(DetailView):
    model = Receipt
    template_name = "receipts/receipt_detail.html"
    context_object_name = "receipt"
    slug_field = "order__order_number"
    slug_url_kwarg = "order_number"

    def get_object(self):
        order_number = self.kwargs.get("order_number")
        order = get_object_or_404(Order, order_number=order_number)
        receipt, _created = Receipt.objects.get_or_create(order=order)
        # generate html snapshot if empty
        if not receipt.html_snapshot:
            context = {
                "order": order,
                "items": order.items.all(),
                "receipt": receipt,
            }
            receipt.html_snapshot = render_to_string(self.template_name, context=context, request=self.request)
            receipt.save(update_fields=["html_snapshot"])
        return receipt

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.object.order
        context["items"] = self.object.order.items.all()
        return context