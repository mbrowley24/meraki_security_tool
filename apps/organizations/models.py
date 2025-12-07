from django.db import models
from django.conf import settings

class OrganizationMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="organization_memberships"
        )
    organization = models.ForeignKey(
        "organizations.Organization", 
        on_delete=models.CASCADE,
        related_name="memberships"
        )
    role = models.CharField(
        max_length=50,
        choices=[
            ("admin", "Admin"),
            ("member", "Member"),
        ],
        default="member"
        )
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class Organization(models.Model):
    public_id = models.UUIDField(
        unique=True,
        editable=False
        )
    name = models.CharField(
        max_length=255, 
        blank=False,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
