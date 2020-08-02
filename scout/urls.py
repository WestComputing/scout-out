from django.urls import path

from .views import LocationFormView, LocationView, render_points_of_interest

app_name = 'scout'
urlpatterns = [
    path('', LocationView.as_view(), name='index'),
    path('location/new/', LocationFormView.as_view(), name='location_new'),
    path('location/<int:location_id>/', render_points_of_interest, name='poi_list')
]
