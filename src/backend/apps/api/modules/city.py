import os

from django.core.exceptions import ObjectDoesNotExist

from apps.api.modules import utilities
from apps.db.City.models import City


api_file = os.path.join(os.path.dirname(__file__), 'yang.gapi')
gc = utilities.GeoCoder(api_file=api_file)


def get_city_instance(address=None,
                      country_name=None, province_name=None, city_name=None,
                      latitude=None, longitude=None):
    if address is None \
            and country_name is not None \
            and province_name is not None \
            and city_name is not None:
        address = ' '.join([country_name, province_name, city_name])
    if address is not None:
        city_dict = gc.address_to_city(address=address)
    else:
        city_dict = gc.gps_to_city(latlng=(latitude, longitude))
    country_name = city_dict['country']
    province_name = city_dict['province']
    city_name = city_dict['city']
    latitude = city_dict['latitude']
    longitude = city_dict['longitude']

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
