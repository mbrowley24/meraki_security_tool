from django.contrib import admin
from .models import FirewallRuleset  
from .models import SSIDConfiguration
from .models import SwitchConfiguration

@admin.register(FirewallRuleset)
class FirewallRulesetAdmin(admin.ModelAdmin):
    # Keep list view lightweight + useful
    list_display = (
        "network",
        "organization_name",
        "last_fetched_at",
        "last_applied_job",
        "rule_count",
        "updated_at",
    )

    list_filter = (
        "last_fetched_at",
        "updated_at",
    )

    search_fields = (
        "network__name",
        "network__network_id",          # if your Network/MerakiNetwork has it
        "network__organization__name",  # adjust if your network FK is named differently
        "last_applied_job__job_name",
        "last_applied_job__public_id",
    )

    ordering = ("-updated_at",)
    list_per_page = 50

    # Speeds up list pages when you show network + org + job
    list_select_related = ("network", "last_applied_job")

    # Don’t let folks accidentally change audit fields
    readonly_fields = ("created_at", "updated_at", "last_fetched_at")

    # If you have many networks, this is huge
    autocomplete_fields = ("network", "last_applied_job")

    fieldsets = (
        ("Scope", {"fields": ("network",)}),
        ("Rules", {"fields": ("rules",)}),
        ("Sync / Audit", {"fields": ("last_fetched_at", "last_applied_job")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Org")
    def organization_name(self, obj):
        # Adjust depending on your network model FK name.
        # If your network model is MerakiNetwork with org FK "organization", this works:
        org = getattr(obj.network, "organization", None)
        if org:
            return org.name

        # If your network model FK is named "orgnization" (typo from earlier), fallback:
        org = getattr(obj.network, "orgnization", None)
        return org.name if org else ""

    @admin.display(description="Rules")
    def rule_count(self, obj):
        # Rules is JSON (likely a list of dicts for MX L3 rules)
        try:
            if isinstance(obj.rules, list):
                return len(obj.rules)
            if isinstance(obj.rules, dict) and "rules" in obj.rules and isinstance(obj.rules["rules"], list):
                return len(obj.rules["rules"])
        except Exception:
            pass
        return "-"


@admin.register(SSIDConfiguration)
class SSIDConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "network",
        "organization_name",
        "last_fetched_at",
        "last_applied_job",
        "ssid_count",
        "updated_at",
    )

    list_filter = (
        "last_fetched_at",
        "updated_at",
    )

    search_fields = (
        "network__name",
        "network__network_id",           # adjust if your Network model uses a different field
        "network__organization__name",   # if FK is organization
        "network__orgnization__name",    # fallback if your FK is still typo'd
        "last_applied_job__job_name",
        "last_applied_job__public_id",
    )

    ordering = ("-updated_at",)
    list_per_page = 50

    # Speed up list view
    list_select_related = ("network", "last_applied_job")

    # Large dropdowns? Make these autocomplete
    autocomplete_fields = ("network", "last_applied_job")

    # Don't edit system-managed fields
    readonly_fields = ("created_at", "updated_at", "last_fetched_at")

    fieldsets = (
        ("Scope", {"fields": ("network",)}),
        ("SSID Configuration", {"fields": ("configuration",)}),
        ("Sync / Audit", {"fields": ("last_fetched_at", "last_applied_job")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Org")
    def organization_name(self, obj):
        # Supports either organization or orgnization on the Network model
        org = getattr(obj.network, "organization", None) or getattr(obj.network, "orgnization", None)
        return org.name if org else ""

    @admin.display(description="SSIDs")
    def ssid_count(self, obj):
        """
        Meraki SSID configs are often a list (0-14) or a dict containing a list.
        This tries to count SSIDs without assuming exact structure.
        """
        try:
            cfg = obj.configuration
            if isinstance(cfg, list):
                return len(cfg)
            if isinstance(cfg, dict):
                # common patterns: {"ssids": [...]} or {"items": [...]}
                for key in ("ssids", "items", "data"):
                    if key in cfg and isinstance(cfg[key], list):
                        return len(cfg[key])
        except Exception:
            pass
        return "-"
    

@admin.register(SwitchConfiguration)
class SwitchConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "network",
        "organization_name",
        "last_fetched_at",
        "last_applied_job",
        "port_count",
        "updated_at",
    )

    list_filter = (
        "last_fetched_at",
        "updated_at",
    )

    search_fields = (
        "network__name",
        "network__network_id",          # adjust if different
        "network__organization__name",  # if network FK is "organization"
        "network__orgnization__name",   # fallback if typo remains
        "last_applied_job__job_name",
        "last_applied_job__public_id",
    )

    ordering = ("-updated_at",)
    list_per_page = 50

    list_select_related = ("network", "last_applied_job")
    autocomplete_fields = ("network", "last_applied_job")

    readonly_fields = ("created_at", "updated_at", "last_fetched_at")

    fieldsets = (
        ("Scope", {"fields": ("network",)}),
        ("Switch Ports", {"fields": ("ports",)}),
        ("Sync / Audit", {"fields": ("last_fetched_at", "last_applied_job")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Org")
    def organization_name(self, obj):
        org = getattr(obj.network, "organization", None) or getattr(obj.network, "orgnization", None)
        return org.name if org else ""

    @admin.display(description="Ports")
    def port_count(self, obj):
        """
        Meraki MS ports endpoint typically returns a list of port dicts.
        This counts ports without assuming exact structure.
        """
        try:
            p = obj.ports
            if isinstance(p, list):
                return len(p)
            if isinstance(p, dict):
                for key in ("ports", "items", "data"):
                    if key in p and isinstance(p[key], list):
                        return len(p[key])
        except Exception:
            pass
        return "-"