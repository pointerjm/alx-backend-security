from django.db import models
from django.utils import timezone


class RequestLog(models.Model):
    """Logs incoming requests with IP, timestamp, path, and geolocation."""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} ({self.country or 'Unknown'})"


class BlockedIP(models.Model):
    """Stores blocked IP addresses."""
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address


class SuspiciousIP(models.Model):
    """Flags IPs showing suspicious activity."""
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"
