
from rest_framework import serializers
from .models import Organization, OrganizationMembership


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['public_id', 'name', 'is_active', 'created_at', 'updated_at']


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = ['user', 'organization', 'role', 'joined_at', 'updated_at']