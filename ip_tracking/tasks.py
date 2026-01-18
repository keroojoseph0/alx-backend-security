from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import SuspiciousIP
from .models import RequestLog
from django.db.models import Count





@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    ip_counts = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=Count('id'))
        .filter(count__gt=100)
    )

    for item in ip_counts:
        SuspiciousIP.objects.get_or_create(
            ip_address=item['ip_address'],
            reason='Exceeded 100 requests per hour'
        )

    sensitive_paths = ['/admin', '/login']

    suspicious_logs = RequestLog.objects.filter(
        created_at__gte=one_hour_ago,
        path__in=sensitive_paths
    )

    for log in suspicious_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f'Accessed sensitive path: {log.path}'
        )
