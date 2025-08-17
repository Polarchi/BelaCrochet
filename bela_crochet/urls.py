"""
URL configuration for bela_crochet.

Este proyecto usa una estructura modular de URLs.
Cada app define sus propias rutas y aquí se incluyen con un prefijo lógico.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django
    path("admin/", admin.site.urls),

    # Páginas principales (homepage, etc.)
    path("", include("pages.urls", namespace="pages")),

    # Catálogo de productos
    path("catalogo/", include("catalog.urls", namespace="catalog")),

    # Detalles de producto (usa un archivo separado product_urls.py dentro de catalog)
    path("producto/", include("catalog.product_urls", namespace="product")),

    # Carrito de compras
    path("carrito/", include("cart.urls", namespace="cart")),

    # Proceso de checkout (pago, confirmación de compra, etc.)
    path("checkout/", include("checkout.urls", namespace="checkout")),

    # Órdenes de los usuarios
    path("ordenes/", include("orders.urls", namespace="orders")),

    # Comprobantes o recibos de pago
    path("comprobante/", include("receipts.urls", namespace="receipts")),

    # Cuentas de usuario (login, registro, perfil, etc.)
    path("cuenta/", include("accounts.urls", namespace="accounts")),
]

# 👇 Esta parte solo se ejecuta en modo DEBUG (desarrollo)
# Sirve archivos de MEDIA (imágenes subidas por usuarios)
# y STATIC (css, js, imágenes estáticas del proyecto)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
