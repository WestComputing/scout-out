from django.db import models


class Geolocation(models.Model):
    place_id = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    formatted_address = models.CharField(max_length=100)
