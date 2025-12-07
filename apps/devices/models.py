from django.db import models
import uuid

class Device(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
        )
    serial_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255, blank=True)
    lan_ip = models.GenericIPAddressField(null=True, blank=True)
    wan_ip = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=32)
    device_type = models.CharField(max_length=100)
    firmware_version = models.CharField(max_length=50)
    product_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"