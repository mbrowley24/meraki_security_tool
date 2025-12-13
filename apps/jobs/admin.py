from django.contrib import admin
from .models import ChangeJob

@admin.register(ChangeJob)
class ChangeJobAdmin(admin.ModelAdmin):
    list_display = (
        "job_name",
        "action",
        "status",
        "organization",
        "network",
        "device",
        "created_by",
        "created_at",
        "started_at",
        "completed_at",
        "has_error",
    )

    list_filter = (
        "status",
        "organization",
        "network",
        "device",
        "created_at",
    )

    search_fields = (
        "public_id",
        "job_name",
        "action",
        "error_message",
        "device__serial_number",   # if Device has it
        "device__name",
        "network__name",           # if MerakiNetwork has it
        "organization__name",      # if Organization has it
        "created_by__username",
        "created_by__email",
    )

    ordering = ("-created_at",)
    list_per_page = 50

    # Don’t show giant JSON on list page; keep it in detail page
    readonly_fields = ("public_id", "created_at", "started_at", "completed_at")

    # Prevent N+1 queries
    list_select_related = ("organization", "network", "device", "created_by")

    # If you have lots of orgs/networks/devices, this makes admin usable
    autocomplete_fields = ("organization", "network", "device", "created_by")

    fieldsets = (
        ("Job", {"fields": ("public_id", "job_name", "action", "status")}),
        ("Scope", {"fields": ("organization", "network", "device", "created_by")}),
        ("Timing", {"fields": ("created_at", "started_at", "completed_at")}),
        ("Payloads", {"fields": ("request_payload", "response_payload")}),
        ("Errors", {"fields": ("error_message",)}),
    )

    @admin.display(boolean=True, description="Error?")
    def has_error(self, obj):
        return bool(obj.error_message)


