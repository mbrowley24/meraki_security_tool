from django.db import models
from ..organizations.models import Organization
import uuid


class MerakiIntegration(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
        )
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        null=False,
    )
    is_active = models.BooleanField(default=True)
    last_verified = models.DateTimeField(null=True, blank=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    last_sync_status = models.CharField(max_length=50, null=True, blank=True)
    last_error_message = models.TextField(null=True, blank=True)
    encrypted_key = models.CharField(max_length=255)
    meraki_organization_id = models.CharField(max_length=255)
    network_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meraki Integration for Org {self.organization_id} and Network {self.network_id}"
