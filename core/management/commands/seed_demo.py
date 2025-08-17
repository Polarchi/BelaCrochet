"""
Management command to populate the database with demo data.

This command creates categories, products with variants and inventory,
some static pages and a demo admin user. It's idempotent: running it
multiple times will not duplicate existing objects.
"""
from __future__ import annotations

import random
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File

from catalog.models import Category, Product, ProductImage, Variant, Inventory
from pages.models import SimplePage


class Command(BaseCommand):
    help = "Seeds the database with demo data for Bela Crochet"

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")
        self.seed_admin()
        self.seed_categories_products()
        self.seed_pages()
        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))

    def seed_admin(self):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            self.stdout.write("Created demo admin user (admin/admin123)")
        else:
            self.stdout.write("Demo admin user already exists")

    def seed_categories_products(self):
        categories_data = [
            ("Gorros", "Accesorios de cabeza"),
            ("Bolsos", "Bolsos y mochilas artesanales"),
            ("Decoración", "Decoración para el hogar"),
        ]
        categories = []
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(name=name, defaults={"meta_description": desc})
            categories.append(cat)
        # Placeholder image path
        placeholder_path = Path(__file__).resolve().parents[4] / "placeholder_light_gray_block.png"
        if not placeholder_path.exists():
            placeholder_path = None
        # create products if not exist
        if Product.objects.exists():
            self.stdout.write("Products already seeded; skipping")
            return
        product_names = [
            "Gorro básico", "Gorro con pompón", "Gorro a rayas", "Bolso playero",
            "Bolso bandolera", "Mochila pequeña", "Cojín decorativo", "Tapete circular",
            "Cesta multiusos", "Mini monedero", "Llaveros", "Individual de mesa",
        ]
        for idx, name in enumerate(product_names):
            category = categories[idx % len(categories)]
            product = Product.objects.create(
                name=name,
                category=category,
                description=f"Descripción de {name.lower()}.",
                price_base=random.choice([10.00, 15.50, 20.00, 25.00]),
            )
            # add placeholder image
            if placeholder_path:
                with open(placeholder_path, "rb") as f:
                    image_file = File(f, name=f"{product.slug}.png")
                    ProductImage.objects.create(product=product, image=image_file, alt_text=product.name)
            # create variants
            variant_names = ["Rojo", "Azul", "Verde"]
            for vname in variant_names:
                sku = f"{product.slug[:3].upper()}-{vname[:2].upper()}-{idx}"
                variant = Variant.objects.create(
                    product=product,
                    name=vname,
                    sku=sku,
                    price_override=None,
                )
                Inventory.objects.create(variant=variant, quantity=random.randint(5, 20), safety_stock=2)
        self.stdout.write(f"Created {len(product_names)} products with variants and inventory")

    def seed_pages(self):
        pages = [
            ("acerca", "Acerca de", "<p>Contenido de la página acerca.</p>"),
            ("contacto", "Contacto", "<p>Contenido de la página contacto.</p>"),
            ("politicas", "Políticas", "<p>Contenido de la página de políticas.</p>"),
            ("tallas", "Guía de tallas", "<p>Contenido de la guía de tallas.</p>"),
        ]
        for slug, title, body in pages:
            SimplePage.objects.get_or_create(slug=slug, defaults={"title": title, "body": body})
        self.stdout.write("Simple pages seeded")