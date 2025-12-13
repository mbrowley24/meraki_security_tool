from django.contrib import admin
from .models import SyncRecord


@admin.register(SyncRecord)
class SyncRecordAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "sync_target",
        "status",
        "triggered_by",
        "networks_fetched",
        "devices_fetched",
        "started_at",
        "completed_at",
        "created_at",
        "has_errors",
    )

    list_filter = (
        "status",
        "sync_target",
        "organization",
        "created_at",
    )

    search_fields = (
        "public_id",
        "organization__name",
        "triggered_by__username",
        "triggered_by__email",
        "error_messages",
    )

    ordering = ("-created_at",)
    list_per_page = 50

    # Speeds up list view
    list_select_related = ("organization", "triggered_by")

    # Makes admin usable when there are many orgs/users
    autocomplete_fields = ("organization", "triggered_by")

    # Prevent edits to system-managed fields
    readonly_fields = ("public_id", "created_at")

    fieldsets = (
        ("Scope", {"fields": ("public_id", "organization", "sync_target", "status", "triggered_by")}),
        ("Progress", {"fields": ("networks_fetched", "devices_fetched")}),
        ("Timing", {"fields": ("started_at", "completed_at", "created_at")}),
        ("Errors", {"fields": ("error_messages",)}),
    )

    @admin.display(boolean=True, description="Errors?")
    def has_errors(self, obj):
        return bool(obj.error_messages)