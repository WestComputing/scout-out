from django.urls import path

from .views import LocationFormView

app_name = 'scout'
urlpatterns = [
    path('', LocationFormView.as_view(), name='index'),
    path('location/new/', LocationFormView.as_view(), name='location_new')
]
