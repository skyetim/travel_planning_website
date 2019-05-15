from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

import apps.api.modules.city as mod_city
import apps.api.modules.user as mod_user
import apps.db.User.models as db_user
from apps.api.modules.exceptions import *


__all__ = []
__all__.extend(['login', 'register', 'reset_password'])
__all__.extend(['get_user_info', 'set_user_info'])
__all__.extend(['address_to_city', 'gps_to_city'])

logged_in_users = {}


def check_authentication(api_func):
    def wrapper(request):
        # check authentication
        # some code here

        # import hashlib
        # md5 = hashlib.md5()
        # for arg in sorted(request.GET.dict().keys()):
        #     if arg != 'key':
        #         continue
        #     md5.update(arg.encode(encoding='UTF-8'))
        #     md5.update(str(request.GET.get(arg)).encode(encoding='UTF-8'))
        # encoded_key = md5.hexdigest()
        # if request.GET.get('key') != encoded_key:
        #     raise

        return api_func(request=request)

    return wrapper


def check_token(api_func):
    def wrapper(request):
        try:
            user_session = db_user.UserSession.objects.get(user_id=int(request.GET.get('user_id')),
                                                           session_id=request.GET.get('session_id'))
        except ObjectDoesNotExist:
            db_user.UserSession.objects.filter(user_id=request.GET.get('user_id')).delete()
            raise UserAuthorizationException('Authorization error.')
        else:
            return api_func(request=request)

    return wrapper


def pack_response(api_func):
    def wrapper(request):
        try:
            response = api_func(request=request)
        except BackendBaseException as e:
            response = {
                'status': e.CODE,
                'error_message': str(e)
            }
        return JsonResponse(response)

    return wrapper


# Create your views here.
@require_http_methods(["GET"])
@pack_response
@check_authentication
def login(request):
    user = mod_user.User(email=str(request.GET.get('email')).lower(),
                         pswd_hash=str(request.GET.get('pswd_hash')).upper())
    logged_in_users[user.get_user_id()] = user

    response = {
        'user_id': user.get_user_id(),
        'session_id': user.get_session_id(),
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@pack_response
@check_authentication
def register(request):
    user = mod_user.User.new_user(email=str(request.GET.get('email')).lower(),
                                  pswd_hash=str(request.GET.get('pswd_hash')).upper(),
                                  user_name=request.GET.get('user_name'),
                                  gender=str(request.GET.get('gender')).upper(),
                                  resident_city_id=int(request.GET.get('resident_city_id')))

    response = {
        'user_id': user.get_user_id(),
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@pack_response
@check_token
@check_authentication
def reset_password(request):
    user = logged_in_users[int(request.GET.get('user_id'))]
    user.reset_password(old_pswd_hash=str(request.GET.get('old_pswd_hash')).upper(),
                        new_pswd_hash=str(request.GET.get('new_pswd_hash')).upper())

    response = {
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@pack_response
@check_token
@check_authentication
def get_user_info(request):
    user = logged_in_users[int(request.GET.get('user_id'))]
    user_info = user.get_user_info()

    response = {
        'user_name': user_info.get_user_name(),
        'email': user.get_email(),
        'gender': user_info.get_gender(),
        'resident_city_id': user_info.get_resident_city_id(),
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@pack_response
@check_token
@check_authentication
def set_user_info(request):
    user = logged_in_users[int(request.GET.get('user_id'))]
    user_info = user.get_user_info()

    user.set_email(email=str(request.GET.get('email')).lower())
    user_info.set_user_name(user_name=request.GET.get('user_name'))
    user_info.set_gender(gender=str(request.GET.get('gender')).upper())
    user_info.set_resident_city_id(resident_city_id=int(request.GET.get('resident_city_id')))

    response = {
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@pack_response
@check_authentication
def address_to_city(request):
    city = mod_city.get_city_instance(address=request.GET.get('address'))

    response = {
        'city_id': city.city_id,
        'country_name': city.country_name,
        'province_name': city.province_name,
        'city_name': city.city_name,
        'latitude': city.latitude,
        'longitude': city.longitude,
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@pack_response
@check_authentication
def gps_to_city(request):
    city = mod_city.get_city_instance(latitude=float(request.GET.get('latitude')),
                                      longitude=float(request.GET.get('longitude')))
    response = {
        'city_id': city.city_id,
        'country_name': city.country_name,
        'province_name': city.province_name,
        'city_name': city.city_name,
        'latitude': city.latitude,
        'longitude': city.longitude,
        'status': 0
    }
    return response
