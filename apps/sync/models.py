from django.conf import settings
from django.db import models
from ..organizations.models import Organization
import uuid

class SyncRecord(models.Model):
    """
    Model to store synchronization records.
    """
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("running", "Running"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("partial", "Partial"),
    )

    TARGET_CHOICES = (
        ("organization", "Organization"),
        ("networks", "Networks"),
        ("devices", "Devices"),
        ("policies", "Policies"),
        ("full", "Full Sync"),
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False, 
        unique=True
        )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='sync_records'
    )

    sync_target = models.CharField(
        max_length=50,
        choices=TARGET_CHOICES,
        default="full"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='triggered_syncs'
    )
    networks_fetched = models.IntegerField(default=0)
    devices_fetched = models.IntegerField(default=0)
    error_messages = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SyncRecord {self.id} - {self.status} at {self.timestamp}"