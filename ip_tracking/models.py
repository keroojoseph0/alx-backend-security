from django.db import models

# Create your models here.
# ip_address,timestamp, path)

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    country = models.CharField(max_length=100, null = True, blank = True)
    city = models.CharField(max_length=100, null = True, blank = True)

    def __str__(self):
        return str(self.ip_address)


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip_address)
    

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"