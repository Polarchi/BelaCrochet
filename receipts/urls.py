from django.urls import path

from .views import ReceiptDetailView


app_name = "receipts"

urlpatterns = [
    path("<str:order_number>/", ReceiptDetailView.as_view(), name="receipt_detail"),
]