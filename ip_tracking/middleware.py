from datetime import datetime
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            request.client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            request.client_ip = request.META.get('REMOTE_ADDR')

        RequestLog.objects.create(
            ip_address = request.client_ip,
            timestamp = datetime.now(),
            path = request.path
        )

        if BlockedIP.objects.filter(ip_address = request.client_ip).exists():
            return HttpResponseForbidden("403 Forbidden")

        response = self.get_response(request)

        return response