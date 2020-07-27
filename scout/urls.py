from django.urls import path

from .views import LocationView

app_name = 'scout'
urlpatterns = [
    path('location/new/', LocationView.as_view(), name='location_new')
]
