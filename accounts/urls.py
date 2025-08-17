from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
    ProfileView,
    AddressListView,
    AddressCreateView,
    AddressUpdateView,
)

app_name = "accounts"

urlpatterns = [
    # Login / Logout
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # Alias en español para login
    path("entrar/", CustomLoginView.as_view(), name="login_es"),
    path("salir/", CustomLogoutView.as_view(), name="logout_es"),

    # Registro
    path("registro/", SignUpView.as_view(), name="signup"),
    # Alias en inglés para registro
    path("signup/", SignUpView.as_view(), name="signup_en"),

    # Perfil
    path("perfil/", ProfileView.as_view(), name="profile"),
    # Alias en inglés para perfil
    path("profile/", ProfileView.as_view(), name="profile_en"),

    # Direcciones
    path("direcciones/", AddressListView.as_view(), name="address_list"),
    path("direcciones/nueva/", AddressCreateView.as_view(), name="address_create"),
    path(
        "direcciones/<int:pk>/editar/",
        AddressUpdateView.as_view(),
        name="address_update",
    ),

    # Alias en inglés para direcciones
    path("addresses/", AddressListView.as_view(), name="address_list_en"),
    path("addresses/new/", AddressCreateView.as_view(), name="address_create_en"),
    path(
        "addresses/<int:pk>/edit/",
        AddressUpdateView.as_view(),
        name="address_update_en",
    ),
]
