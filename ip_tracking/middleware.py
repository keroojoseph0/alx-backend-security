import requests
from django.conf import settings
from django.core.cache import cache
from .models import RequestLog
from datetime import datetime

class IPLoggingMiddleware:
    """
    Logs IP, path, and geolocation info for each request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        country, city = self.get_geolocation(ip)

        # Save log
        try:
            RequestLog.objects.create(
                ip_address=str(ip),
                path=str(request.path),
                country=str(country or ''),
                city=str(city or '')
            )
        except Exception as e:
            print(type(country), type(city), country, city)
            raise e

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_geolocation(self, ip):
        """Fetch geolocation from cache or API"""
        cache_key = f"geo_{ip}"
        cached = cache.get(cache_key)
        if cached:
            return cached['country'], cached['city']

        # Call IPGeolocation API
        try:
            url = f"https://api.ipgeolocationapi.com/geolocate/{ip}"
            headers = {"Accept": "application/json", "Authorization": f"Bearer {settings.IPGEOLOCATION_API_KEY}"}
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            country = data.get('country', '')
            city = data.get('city', '')

            # Cache for 24 hours
            cache.set(cache_key, {'country': country, 'city': city}, 24 * 3600)
            return country, city
        except Exception:
            return '', ''
