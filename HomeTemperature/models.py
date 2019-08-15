from django.db import models


class TemperatureData(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    humidity = models.DecimalField(max_digits=4, decimal_places=2, null=True)

