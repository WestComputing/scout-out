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

    def __str__(self):
        return f"{self.formatted_address}: {self.lat}, {self.lon}"


class UserGeolocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='users')
    geolocation = models.ForeignKey(Geolocation, on_delete=models.CASCADE,
                                    related_name='geolocations')
    label = models.CharField(max_length=50, default="Home")

    class Meta:
        unique_together = ('user', 'label')

    def __str__(self):
        return f"{self.label}: {self.geolocation.city}, {self.geolocation.state} " \
               f"{self.geolocation.zip_code} ({self.user.username})"

# class RecArea(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     directions = models.CharField(max_length=250)
#     phone = models.CharField(max_length=20)
#     email = models.CharField(max_length=50)
#     lat = models.DecimalField(max_digits=8, decimal_places=6)
#     lon = models.DecimalField(max_digits=9, decimal_places=6)
#     url = models.CharField(max_length=250)
