from django.urls import path

from .views import LocationFormView, LocationView

app_name = 'scout'
urlpatterns = [
    path('', LocationView.as_view(), name='index'),
    path('location/new/', LocationFormView.as_view(), name='location_new')
]
