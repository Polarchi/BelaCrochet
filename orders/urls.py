from django.urls import path

from .views import OrderListView, OrderDetailView


app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("<str:order_number>/", OrderDetailView.as_view(), name="order_detail"),
]