from django.db import models
from apps.jobs.models import ChangeJob
from apps.networks.models import MerakiNetwork as Network

class FirewallRuleset(models.Model):
    # last known good configuration from a Meraki MX firewall

    network = models.OneToOneField(
        Network,
        on_delete=models.CASCADE,
        related_name='firewall_ruleset'
    )

    rules = models.JSONField()

    last_fetched_at = models.DateTimeField(null=True, blank=True)

    last_applied_job = models.ForeignKey(
        ChangeJob,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='firewall_updates'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'FirewallRuleset for {self.network.name}'


class SSIDConfiguration(models.Model):
    # last known good configuration from a Meraki MR SSID

    network = models.OneToOneField(
        Network,
        on_delete=models.CASCADE,
        related_name='ssid_configurations'
    )


    configuration = models.JSONField()

    last_fetched_at = models.DateTimeField(null=True, blank=True)

    last_applied_job = models.ForeignKey(
        ChangeJob,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='ssid_updates'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

        


    def __str__(self):
        return f'SSIDConfiguration for SSID {self.ssid_number} on {self.network.name}'

class SwitchConfiguration(models.Model):
    # last known good configuration from a Meraki MS switch

    network = models.OneToOneField(
        Network,
        on_delete=models.CASCADE,
        related_name='switch_configuration'
    )

    ports = models.JSONField()

    last_fetched_at = models.DateTimeField(null=True, blank=True)

    last_applied_job = models.ForeignKey(
        ChangeJob,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='switch_updates'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'SwitchConfiguration for {self.network.name}'