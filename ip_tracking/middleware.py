from django.utils import timezone
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.core.cache import cache
from .models import RequestLog, BlockedIP


class IPTrackingMiddleware:
    """
    Middleware for:
    - Logging request IP, path, and timestamp
    - Adding GeoIP country/city info
    - Blocking blacklisted IPs
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.geo = GeoIP2()

    def __call__(self, request):
        # --- Get client IP ---
        client_ip, _ = get_client_ip(request)
        if client_ip is None:
            client_ip = "0.0.0.0"

        # --- Check blacklist ---
        if BlockedIP.objects.filter(ip_address=client_ip).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")

        # --- Try cached geo info ---
        cached_data = cache.get(client_ip)
        if cached_data:
            country, city = cached_data
        else:
            country, city = None, None
            try:
                geo_data = self.geo.city(client_ip)
                country = geo_data.get("country_name")
                city = geo_data.get("city")
                cache.set(client_ip, (country, city), 60 * 60 * 24)  # cache for 24 hours
            except Exception:
                # GeoIP lookup might fail for localhost or private IPs
                pass

        # --- Log request ---
        RequestLog.objects.create(
            ip_address=client_ip,
            path=request.path,
            timestamp=timezone.now(),
            country=country,
            city=city
        )

        # --- Continue request cycle ---
        response = self.get_response(request)
        return response
