from django.contrib import admin
from .models import SimplePage


@admin.register(SimplePage)
class SimplePageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("is_active",)
    search_fields = ("title",)