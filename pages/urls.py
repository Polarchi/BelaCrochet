from django.urls import path

from .views import (
    HomePageView,
    AboutPageView,
    ContactPageView,
    PoliciesPageView,
    SizesPageView,
    SimplePageDetailView,
)


app_name = "pages"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("acerca/", AboutPageView.as_view(), name="about"),
    path("contacto/", ContactPageView.as_view(), name="contact"),
    path("politicas/", PoliciesPageView.as_view(), name="policies"),
    path("tallas/", SizesPageView.as_view(), name="sizes"),
    path("p/<slug:slug>/", SimplePageDetailView.as_view(), name="detail"),
]