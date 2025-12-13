from django.contrib import admin
from .models import MerakiNetwork

@admin.register(MerakiNetwork)
class MerakiNetworkAdmin(admin.ModelAdmin):
    # Columns shown in list view
    list_display = (
        "name",
        "network_id",
        "organization",
        "meraki_organization_id",
        "is_active",
        "time_zone",
        "created_at",
    )

    # Right-side filters
    list_filter = (
        "organization",
        "is_active",
        "time_zone",
        "created_at",
    )

    # Search box (supports relations via __)
    search_fields = (
        "name",
        "network_id",
        "meraki_organization_id",
        "organization__name",
        "public_id",
    )

    # Default ordering
    ordering = ("name",)

    # Avoid N+1 queries
    list_select_related = ("organization",)

    # Protect system-managed / immutable fields
    readonly_fields = (
        "public_id",
        "created_at",
    )

    # Large org lists? Make this searchable instead of dropdown
    autocomplete_fields = ("organization",)

    # Pagination
    list_per_page = 50

    # Admin form layout
    fieldsets = (
        ("Identity", {"fields": ("public_id", "name", "network_id")}),
        ("Organization", {"fields": ("organization", "meraki_organization_id")}),
        ("Configuration", {"fields": ("time_zone", "product_types", "is_active")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )
