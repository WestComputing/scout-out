from django.urls import path

from .views import LocationFormView

app_name = 'scout'
urlpatterns = [
    path('location/new/', LocationFormView.as_view(), name='location_new')
]
