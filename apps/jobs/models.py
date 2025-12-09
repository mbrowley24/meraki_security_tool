from django.db import models
from django.conf import settings
from ..organizations.models import Organization
from ..networks.models import MerakiNetwork
from ..devices.models import Device
import uuid


class ChangeJob(models.Model):
    
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("running", "Running"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            null= True,
            on_delete=models.SET_NULL,
            related_name='jobs'
            )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    network = models.ForeignKey(
        MerakiNetwork,
        on_delete= models.CASCADE,
        related_name='jobs'
    )

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    action = models.CharField(blank=False)
    status = models.CharField(
        max_length=50,
        blank=False,
        choices=STATUS_CHOICES,
        default="pending"
    )

    request_payload = models.JSONField()
    response_payload = models.JSONField(null=True, blank=True)
    job_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.status}"