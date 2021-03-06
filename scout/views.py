import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView, DeleteView

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


class UserOwnsItem(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user


class LocationFormView(LoginRequiredMixin, FormView):
    template_name = 'scout/location_form.html'
    form_class = LocationForm
    success_url = reverse_lazy('scout:index')

    def form_valid(self, form):
        user = self.request.user
        zip_code = form.cleaned_data.get('zip_code')
        city = form.cleaned_data.get("city")
        state = form.cleaned_data.get("state")
        label = form.cleaned_data.get('label')
        if not label:
            if city:
                label = f"{city}, {state}"
            else:
                label = zip_code
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


class LocationDeleteFormView(LoginRequiredMixin, UserOwnsItem, DeleteView):
    model = Geolocation
    success_url = reverse_lazy('scout:index')


def get_recdata(lat, lon, url):
    params = dict(full='true', radius='50', latitude=lat, longitude=lon)
    headers = dict(apikey=settings.API_KEY_RECREATION_GOV)
    response = requests.get(url, params=params, headers=headers)
    recdata = []
    if response.ok:
        response_json = response.json()
        recdata = response_json.get('RECDATA', [])
    return recdata


def get_rec_areas(lat: str, lon: str) -> list:
    url = f"https://ridb.recreation.gov/api/v1/recareas?"
    return get_recdata(lat, lon, url)


def get_facilities(lat: str, lon: str) -> list:
    url = f"https://ridb.recreation.gov/api/v1/facilities?"
    return get_recdata(lat, lon, url)


def get_facility(facility_id: str) -> dict:
    url = f"https://ridb.recreation.gov/api/v1/facilities/{facility_id}"
    headers = dict(apikey=settings.API_KEY_RECREATION_GOV)
    response = requests.get(url, headers=headers)
    facility = {}
    if response.ok:
        facility.update(response.json())
    return facility


def render_facility(request, facility_id: str):
    return render(request, 'scout/facility.html', dict(facility=get_facility(facility_id)))


def get_campsites(facility_id: str) -> list:
    url = f"https://ridb.recreation.gov/api/v1/facilities/{facility_id}/campsites?"
    params = dict(full='true', radius='50')
    headers = dict(apikey=settings.API_KEY_RECREATION_GOV)
    response = requests.get(url, params=params, headers=headers)
    campsites = []
    if response.ok:
        response_json = response.json()
        campsites = response_json.get('RECDATA', [])
    return campsites


def render_points_of_interest(request, location_id):
    location = get_object_or_404(Geolocation, id=location_id)
    coords = (str(location.lat), str(location.lon))
    rec_areas = get_rec_areas(*coords)
    facilities = get_facilities(*coords)
    campsites = []
    for facility in facilities:
        campsites.extend(get_campsites(facility['FacilityID']))
    return render(request, 'scout/poi_list.html', dict(location=location,
                                                       rec_areas=rec_areas,
                                                       facilities=facilities,
                                                       campsites=campsites
                                                       ))
