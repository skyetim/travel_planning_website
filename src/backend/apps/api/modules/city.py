import os

import apps.db.City.models as db_city
from apps.api.modules import utilities
from apps.api.modules.exceptions import *


api_file = os.path.join(os.path.dirname(__file__), 'yang.gapi')
gc = utilities.GeoCoder(api_file=api_file)


def get_city_instance_list_by_address(address):
    city_dict_list = gc.address_to_city_list(address=address)

    city_list = []

    for city_dict in city_dict_list:
        try:
            country_name = city_dict['country']
            province_name = city_dict['province']
            city_name = city_dict['city']
            latitude = city_dict['latitude']
            longitude = city_dict['longitude']
        except KeyError:
            continue

        try:
            city = db_city.City.objects.get(country_name=country_name,
                                            province_name=province_name,
                                            city_name=city_name)
        except db_city.City.DoesNotExist:
            city = db_city.City.objects.create(country_name=country_name,
                                               province_name=province_name,
                                               city_name=city_name,
                                               latitude=latitude,
                                               longitude=longitude)
        city_list.append(city)

    return city_list


def get_city_instance_by_address(address):
    city_dict = gc.address_to_city(address=address)

    try:
        country_name = city_dict['country']
        province_name = city_dict['province']
        city_name = city_dict['city']
        latitude = city_dict['latitude']
        longitude = city_dict['longitude']
    except KeyError:
        raise NoCityFoundException(f'No city found near address "{address}".')

    try:
        city = db_city.City.objects.get(country_name=country_name,
                                        province_name=province_name,
                                        city_name=city_name)
    except db_city.City.DoesNotExist:
        city = db_city.City.objects.create(country_name=country_name,
                                           province_name=province_name,
                                           city_name=city_name,
                                           latitude=latitude,
                                           longitude=longitude)
    return city


def get_city_instance_by_gps(latitude, longitude):
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
        raise NoCityFoundException(f'No city found near location {(latitude, longitude)}.')

    try:
        city = db_city.City.objects.get(country_name=country_name,
                                        province_name=province_name,
                                        city_name=city_name)
    except db_city.City.DoesNotExist:
        city = db_city.City.objects.create(country_name=country_name,
                                           province_name=province_name,
                                           city_name=city_name,
                                           latitude=latitude,
                                           longitude=longitude)
    return city


def get_city_instance_by_id(city_id):
    try:
        city = db_city.City.objects.get(city_id=city_id)
    except db_city.City.DoesNotExist:
        raise CityIdDoesNotExistException(f'City (ID={city_id}) does not exist.')
    return city
