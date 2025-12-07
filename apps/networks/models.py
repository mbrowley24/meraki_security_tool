from django.db import models
from ..organizations.models import Organization
import uuid


class MerakiProductTypes(models.TextChoices):
    APPLIANCE = 'appliance', 'Appliance'
    CAMERA = 'camera', 'Camera'
    SWITCH = 'switch', 'Switch'
    WIRELESS = 'wireless', 'Wireless'
    SENSOR = 'sensor', 'Sensor'

class MerakiNetwork(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False, 
        unique=True
        )
    orgnization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='networks'
    )
    meraki_orgnization_id = models.CharField(max_length=50)
    network_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    time_zone = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    product_types = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.network_id})"
