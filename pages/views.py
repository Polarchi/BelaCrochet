"""
Views for marketing and informational pages.
"""
from __future__ import annotations

from django.views.generic import TemplateView, DetailView

from catalog.models import Product
from .models import SimplePage


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured products: latest 8 active products
        context["featured_products"] = Product.objects.filter(is_active=True).order_by("-id")[:8]
        return context


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class ContactPageView(TemplateView):
    template_name = "pages/contact.html"


class PoliciesPageView(TemplateView):
    template_name = "pages/policies.html"


class SizesPageView(TemplateView):
    template_name = "pages/sizes.html"


class SimplePageDetailView(DetailView):
    model = SimplePage
    template_name = "pages/simple_page.html"
    context_object_name = "page"
    slug_url_kwarg = "slug"