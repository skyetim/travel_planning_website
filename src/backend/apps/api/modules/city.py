import os

from django.core.exceptions import ObjectDoesNotExist

from apps.api.modules import utilities
from apps.db.City.models import City


api_file = os.path.join(os.path.dirname(__file__), 'yang.gapi')
gc = utilities.GeoCoder(api_file=api_file)


def address_to_city_instance(address):
    city_address = gc.address_to_city(address=address)
    country_name = city_address['country']
    province_name = city_address['admin_area_1']
    city_name = city_address['locality']
    latitude = city_address['latitude']
    longitude = city_address['longitude']

    # address = f'{country_name} {province_name} {city_name}'
    # latitude, longitude = gc.address_to_gps(address=address)
    try:
        city = City.objects.get(country_name=country_name,
                                province_name=province_name,
                                city_name=city_name)
    except ObjectDoesNotExist:
        city = City.objects.create(country_name=country_name,
                                   province_name=province_name,
                                   city_name=city_name,
                                   latitude=latitude,
                                   longitude=longitude)
    return city
