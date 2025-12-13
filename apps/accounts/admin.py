from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    # Columns in the list page
    list_display = ("user", "email", "organization", "public_id")

    # Right-side filters
    list_filter = ("organization",)

    # Search box (supports related fields via __)
    search_fields = (
        "public_id",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

     # Default sort
    ordering = ("user__username",)

    # Protect immutable fields
    readonly_fields = ("public_id",)

    # Use autocomplete instead of huge dropdowns (requires org admin search_fields)
    autocomplete_fields = ("organization",)

    # Small quality-of-life: reduce DB queries when listing
    list_select_related = ("user", "organization")


    # Optional: show user fields grouped nicely
    fieldsets = (
        ("Identity", {"fields": ("user", "public_id")}),
        ("Tenant", {"fields": ("organization",)}),
    )

    @admin.display(description="Email")
    def email(self, obj):
        return getattr(obj.user, "email", "")
