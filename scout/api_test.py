import os

API_KEY_GOOGLE = os.environ['API_KEY_GOOGLE']


def get_geocode(payload: dict) -> (str, dict):
    """
{
   "results": [],
   "status": "ZERO_RESULTS"
}

{
   "error_message": "Invalid request. Missing the 'address', 'components',
                    'latlng' or 'place_id' parameter.",
   "results": [],
   "status": "INVALID_REQUEST"
}
    response.ok: bool
    response.status_code: int
    response.reason: str
    :payload: dict {city: str, state: str, zip_code: str}
    :return: dict content
    """
    # if "zip_code" in payload:
    #     params = {"components": f"postal_code:{payload['zip_code']}"}
    # else:
    #     params = {"address": f"{payload['city']},{payload['state']}"}
    # params.update({"key": API_KEY_GOOGLE})
    # url = f"https://maps.googleapis.com/maps/api/geocode/json"
    # response = requests.get(url, params=params)
    # if response.ok:
    #     response_json = response.json()
    #     status = response_json.get('status')
    #     results = response_json.get('results', [])[0]
    # else:
    #     status = f"{response.status_code}: {response.reason}"
    #     results = []
    # return status, results


results_ = \
    [{
        'address_components': [
            {'long_name': 'Browns Summit', 'short_name': 'Browns Summit', 'types': ['locality', 'political']},
            {'long_name': 'Monroe', 'short_name': 'Monroe', 'types': ['administrative_area_level_3', 'political']},
            {'long_name': 'Guilford County', 'short_name': 'Guilford County',
             'types': ['administrative_area_level_2', 'political']},
            {'long_name': 'North Carolina', 'short_name': 'NC', 'types': ['administrative_area_level_1', 'political']},
            {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']},
            {'long_name': '27214', 'short_name': '27214', 'types': ['postal_code']}
        ],
        'formatted_address': 'Browns Summit, NC 27214, USA',
        'geometry': {
            'bounds': {'northeast': {'lat': 36.2263112, 'lng': -79.699112},
                       'southwest': {'lat': 36.2039131, 'lng': -79.72193589999999}},
            'location': {'lat': 36.2127803, 'lng': -79.7131567},
            'location_type': 'APPROXIMATE',
            'viewport': {'northeast': {'lat': 36.2263112, 'lng': -79.699112},
                         'southwest': {'lat': 36.2039131, 'lng': -79.72193589999999}}},
        'place_id': 'ChIJQYERvEveUogR7GobOJ1EwTs', 'types': ['locality', 'political']
    }]

if __name__ == '__main__':
    location = {'city': 'browns summit', 'state': 'nc'}
    location = {'zip_code': '60603', 'state': 'IL'}
    print(get_geocode(location))

    # json_response = response.json()
    # extended_data = {}
    # if "status" in json_response.keys() and json_response['status'] == "OK":
    #     if "results" in json_response.keys() and json_response['results']:
    #         results = json_response['results'][0]
    #         if "formatted_address" in results:
    #             extended_data['formatted_address'] = results['formatted_address']
    #         if "geometry" in results:
    #             extended_data['lat'] = Decimal(results['geometry']['location']['lat']).quantize(Decimal('1.000000'))
    #             extended_data['lon'] = Decimal(results['geometry']['location']['lng']).quantize(Decimal('1.000000'))
    #         # if "address_components" in results and results['address_components']:
    #         #     extended_data['zip_code'] = results['address_components'][0]['short_name']
    #         if "address_components" in results and len(results['address_components']) > 3:
    #             extended_data['state'] = results['address_components'][3]['short_name']
    # return extended_data
