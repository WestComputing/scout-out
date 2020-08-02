from django.contrib.auth.models import User
from django.db import models


class Geolocation(models.Model):
    place_id = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    formatted_address = models.CharField(max_length=100)
    label = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return f"{self.label}: " \
               f"{self.formatted_address}, " \
               f"{self.lat} x {self.lon} " \
               f"({self.user.username})"
