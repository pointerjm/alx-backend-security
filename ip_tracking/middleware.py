import logging
from django.utils import timezone
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from django.core.cache import cache
from .models import RequestLog, BlockedIP

logger = logging.getLogger(__name__)

class IPTrackingMiddleware:
    """
    Middleware for:
    - Logging request IP, path, and timestamp
    - Adding GeoIP country/city info
    - Blocking blacklisted IPs
    """

    def __init__(self, get_response):
        self.get_response = get_response
        try:
            self.geo = GeoIP2()
        except GeoIP2Exception as e:
            logger.error(f"GeoIP2 initialization failed: {e}")
            self.geo = None
        except Exception as e:
            logger.exception(f"Unexpected error initializing GeoIP2: {e}")
            self.geo = None

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
            if self.geo:
                try:
                    geo_data = self.geo.city(client_ip)
                    country = geo_data.get("country_name")
                    city = geo_data.get("city")
                    cache.set(client_ip, (country, city), 60 * 60 * 24)  # cache for 24 hours
                except Exception as e:
                    logger.warning(f"GeoIP lookup failed for {client_ip}: {e}")

        # --- Log request ---
        try:
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path,
                timestamp=timezone.now(),
                country=country,
                city=city
            )
        except Exception as e:
            logger.error(f"Failed to log request for {client_ip}: {e}")

        # --- Continue request cycle ---
        return self.get_response(request)
