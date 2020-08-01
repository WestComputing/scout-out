import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from .forms import LocationForm
from .models import Geolocation


def get_geocode(payload: dict) -> (str, dict):
    if "zip_code" in payload:
        params = dict(components=f"postal_code:{payload['zip_code']}")
    else:
        params = dict(address=f"{payload['city']},{payload['state']}")
    params.update({"key": settings.API_KEY_GOOGLE})
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(url, params=params)
    record = {}
    if response.ok:
        response_json = response.json()
        status = response_json.get('status')
        results = response_json.get('results', [])[0]
        if status == 'OK':
            record = dict(place_id=results['place_id'],
                          formatted_address=results['formatted_address'],
                          lat=results['geometry']['location']['lat'],
                          lon=results['geometry']['location']['lng']
                          )
            fields_map = dict(postal_code='zip_code',
                              locality='city',
                              administrative_area_level_1='state'
                              )
            for component in results['address_components']:
                for k, v in fields_map.items():
                    if k in component['types']:
                        record.update({v: component['short_name']})
    else:
        status = f"{response.status_code}: {response.reason}"
    return status, record


def get_rec_areas(lat: str, lon: str):
    url = f"https://ridb.recreation.gov/api/v1/recareas?"
    params = dict(full='true', radius='50', latitude=lat, longitude=lon)
    headers = dict(apikey=settings.API_KEY_RECREATION_GOV)
    response = requests.get(url, params=params, headers=headers)
    rec_areas = []
    if response.ok:
        response_json = response.json()
        rec_areas = response_json.get('RECDATA', [])
    return rec_areas


class LocationFormView(LoginRequiredMixin, FormView):
    template_name = 'scout/location_form.html'
    form_class = LocationForm
    success_url = reverse_lazy('scout:index')

    def form_valid(self, form):
        user = self.request.user
        label = form.cleaned_data.get('label')
        zip_code = form.cleaned_data.get('zip_code')
        city = form.cleaned_data.get("city")
        state = form.cleaned_data.get("state")
        if zip_code:
            status, record = get_geocode(dict(zip_code=zip_code))
        else:
            status, record = get_geocode(dict(city=city, state=state))
        geolocation = Geolocation(user=user, label=label, **record)
        geolocation.save()
        return super().form_valid(form)


class LocationView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    context_object_name = 'locations'

    def get_queryset(self):
        return Geolocation.objects \
            .filter(user_id=self.request.user.id).order_by('label')
