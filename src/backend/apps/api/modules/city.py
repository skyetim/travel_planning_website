import os

from django.core.exceptions import ObjectDoesNotExist

import apps.db.City.models as db_city
from apps.api.modules import utilities
from apps.api.modules.exceptions import *


api_file = os.path.join(os.path.dirname(__file__), 'yang.gapi')
gc = utilities.GeoCoder(api_file=api_file)


def get_or_create_city_instance(address=None,
                                country_name=None, province_name=None, city_name=None,
                                latitude=None, longitude=None):
    if address is None \
            and country_name is not None \
            and province_name is not None \
            and city_name is not None:
        address = ' '.join([country_name, province_name, city_name])
    from_address = True
    if address is not None:
        city_dict = gc.address_to_city(address=address)
    else:
        from_address = False
        try:
            city_dict = gc.gps_to_city(latlng=(latitude, longitude))
        except KeyError:
            raise NoCityFoundException(f'No city found near location {(latitude, longitude)}.')

    try:
        country_name = city_dict['country']
        province_name = city_dict['province']
        city_name = city_dict['city']
        latitude = city_dict['latitude']
        longitude = city_dict['longitude']
    except KeyError:
        if from_address:
            raise NoCityFoundException(f'No city found near address "{address}".')
        else:
            raise NoCityFoundException(f'No city found near location {(latitude, longitude)}.')

    try:
        city = db_city.City.objects.get(country_name=country_name,
                                        province_name=province_name,
                                        city_name=city_name)
    except ObjectDoesNotExist:
        city = db_city.City.objects.create(country_name=country_name,
                                           province_name=province_name,
                                           city_name=city_name,
                                           latitude=latitude,
                                           longitude=longitude)
    return city


def get_city_instance_by_id(city_id):
    try:
        city = db_city.City.objects.get(city_id=city_id)
    except ObjectDoesNotExist:
        raise CityIdDoesNotExistException(f'City (ID={city_id}) does not exist.')
    return city
