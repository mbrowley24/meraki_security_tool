from django.db import models
from django.conf import settings
from ..organizations.models import Organization
import uuid

class UserProfile(models.Model):
    user      = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name='user_profiles',
        null=True,
        )


    def __str__(self):
        return f"{self.user.username}'s profile"
