from django.contrib import admin
from .models import MerakiIntegration


@admin.register(MerakiIntegration)
class MerakiIntegrationAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "is_active",
        "meraki_organization_id",
        "network_id",
        "last_verified",
        "last_sync_at",
        "last_sync_status",
        "has_error",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "last_sync_status",
        "last_verified",
        "last_sync_at",
    )

    search_fields = (
        "public_id",
        "organization__name",          # if Organization has name
        "meraki_organization_id",
        "network_id",
    )

    ordering = ("-updated_at",)

    # Avoid N+1 queries
    list_select_related = ("organization",)

    # Protect sensitive + system-managed fields
    readonly_fields = (
        "public_id",
        "created_at",
        "updated_at",
        "last_verified",
        "last_sync_at",
        "last_sync_status",
        "last_error_message",
    )

    # Prevent leaking secrets in list view (don’t include encrypted_key there)
    # Optionally: allow editing only if you explicitly need it
    fieldsets = (
        ("Linkage", {"fields": ("public_id", "organization", "is_active")}),
        ("Meraki Identifiers", {"fields": ("meraki_organization_id", "network_id")}),
        ("Credentials", {"fields": ("encrypted_key",)}),
        ("Sync Health", {"fields": ("last_verified", "last_sync_at", "last_sync_status", "last_error_message")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(boolean=True, description="Error?")
    def has_error(self, obj):
        return bool(obj.last_error_message)
