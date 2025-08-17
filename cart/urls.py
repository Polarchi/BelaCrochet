from django.urls import path

from .views import CartDetailView, AddToCartView, UpdateCartItemView, RemoveCartItemView


app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart_detail"),
    path("agregar/<slug:product_slug>/", AddToCartView.as_view(), name="add_to_cart"),
    path("actualizar/<int:item_id>/", UpdateCartItemView.as_view(), name="update_item"),
    path("eliminar/<int:item_id>/", RemoveCartItemView.as_view(), name="remove_item"),
]