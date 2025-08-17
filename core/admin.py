from django.contrib import admin

from .models import MediaImage, SiteSetting


@admin.register(MediaImage)
class MediaImageAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "alt_text")
    search_fields = ("name", "alt_text")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = (
        "brand_name",
        "palette_primary",
        "palette_secondary",
        "palette_accent",
    )
    fieldsets = (
        (None, {"fields": ("brand_name", "logo")}),
        (
            "Colours",
            {
                "fields": (
                    "palette_primary",
                    "palette_secondary",
                    "palette_accent",
                )
            },
        ),
        (
            "Social",
            {"fields": ("facebook", "instagram", "tiktok")},
        ),
    )