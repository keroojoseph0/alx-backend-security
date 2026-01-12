from django.db import models

# Create your models here.
# ip_address,timestamp, path)

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    path = models.TextField()