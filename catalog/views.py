"""
Views for catalogue browsing and product details.
"""
from __future__ import annotations

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        order = self.request.GET.get("orden")
        if order == "precio":
            queryset = queryset.order_by("price_base")
        elif order == "precio_desc":
            queryset = queryset.order_by("-price_base")
        else:
            queryset = queryset.order_by("name")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category_slug"] = self.kwargs.get("category_slug")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # first image as main image
        context["main_image"] = self.object.images.first()
        context["variants"] = self.object.variants.all()
        return context