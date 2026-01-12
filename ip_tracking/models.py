from django.db import models

# Create your models here.
# ip_address,timestamp, path)

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    path = models.TextField()

    def __str__(self):
        return str(self.ip_address)


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip_address)
    