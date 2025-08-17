from django.urls import path

from .views import ProductListView


app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("categoria/<slug:category_slug>/", ProductListView.as_view(), name="product_list_by_category"),
]