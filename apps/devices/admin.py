from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    # List page columns
    list_display = (
        "name",
        "serial_number",
        "device_type",
        "product_type",
        "firmware_version",
        "lan_ip",
        "wan_ip",
        "mac_address",
        "is_active",
        "updated_at",
    )

    # Right sidebar filters
    list_filter = (
        "is_active",
        "device_type",
        "product_type",
        "firmware_version",
    )

    # Search box (supports partial matches)
    search_fields = (
        "serial_number",
        "mac_address",
        "name",
        "lan_ip",
        "wan_ip",
        "location",
        "public_id",
    )

    # Default ordering
    ordering = ("-updated_at",)

    # Prevent accidental edits to stable identifiers
    readonly_fields = ("public_id", "created_at", "updated_at", "serial_number", "mac_address")

    # Make common toggles editable right from the list view (optional)
    list_editable = ("is_active",)

    # Pagination
    list_per_page = 50

    # Nice form layout
    fieldsets = (
        ("Identity", {"fields": ("public_id", "serial_number", "mac_address", "name")}),
        ("Classification", {"fields": ("device_type", "product_type", "firmware_version", "is_active")}),
        ("Networking", {"fields": ("lan_ip", "wan_ip", "location")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )