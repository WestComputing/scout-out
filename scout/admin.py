from django.contrib import admin

from .models import Geolocation, UserGeolocation

admin.site.register(Geolocation)
admin.site.register(UserGeolocation)
