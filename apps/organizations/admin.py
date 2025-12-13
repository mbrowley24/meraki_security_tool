from django.contrib import admin
from .models import Organization, OrganizationMembership

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "public_id", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "public_id")

    ordering = ("name",)
    list_per_page = 50

    # Protect IDs + timestamps
    readonly_fields = ("public_id", "created_at", "updated_at")

    # Optional: nicer layout
    fieldsets = (
        ("Organization", {"fields": ("name", "is_active")}),
        ("System", {"fields": ("public_id", "created_at", "updated_at")}),
    )



    from .models import OrganizationMembership  # adjust import path


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "user_email", "organization", "role", "joined_at", "updated_at")
    list_filter = ("role", "organization", "joined_at")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "organization__name",
    )
    ordering = ("organization__name", "user__username")
    list_per_page = 50

    # Makes admin fast (avoid N+1 queries)
    list_select_related = ("user", "organization")

    # Much nicer than huge dropdowns
    autocomplete_fields = ("user", "organization")

    # Usually you don’t want people editing timestamps
    readonly_fields = ("joined_at", "updated_at")

    fieldsets = (
        ("Membership", {"fields": ("user", "organization", "role")}),
        ("Timestamps", {"fields": ("joined_at", "updated_at")}),
    )

    @admin.display(description="Email")
    def user_email(self, obj):
        return getattr(obj.user, "email", "")
