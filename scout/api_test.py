import os

import requests

API_KEY_GOOGLE = os.environ['API_KEY_GOOGLE']
API_KEY_RECREATION_GOV = os.environ['API_KEY_RECREATION_GOV']


def get_rec_areas(lat, lon):
    url = f"https://ridb.recreation.gov/api/v1/recareas?" \
          f"full=true&latitude={str(lat)}&longitude={str(lon)}&radius=50"
    headers = {'apikey': API_KEY_RECREATION_GOV}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()['RECDATA']
    else:
        print(response)


if __name__ == '__main__':
    rec_areas = get_rec_areas(41.880916, -87.625425)
    print(rec_areas)
