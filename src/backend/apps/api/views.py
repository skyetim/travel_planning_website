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


def prepare_request_data(api_func):
    def prd_wrapper(request):
        def cast(name, cast_func):
            if name in request_data:
                request_data[name] = cast_func(request_data[name])

        request_data = request.GET.dict()
        cast(name='user_id', cast_func=int)
        cast(name='email', cast_func=str.lower)
        cast(name='email', cast_func=str.lower)
        cast(name='pswd_hash', cast_func=str.upper)
        cast(name='old_pswd_hash', cast_func=str.upper)
        cast(name='new_pswd_hash', cast_func=str.upper)
        cast(name='city_id', cast_func=int)
        cast(name='resident_city_id', cast_func=int)
        cast(name='latitude', cast_func=float)
        cast(name='longitude', cast_func=float)

        return api_func(request_data=request_data)

    return prd_wrapper


def check_authentication(api_func):
    def ca_wrapper(request_data):
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

        return api_func(request_data=request_data)

    return ca_wrapper


def check_token(api_func):
    def ck_wrapper(request_data):
        user_id = request_data['user_id'],
        session_id = request_data['session_id']
        try:
            user_session = db_user.UserSession.objects.get(user_id=user_id,
                                                           session_id=session_id)
        except ObjectDoesNotExist:
            db_user.UserSession.objects.filter(user_id=user_id).delete()
            raise UserAuthorizationException(f'User (ID={user_id}) and session (ID={session_id}) do not match.')
        else:
            return api_func(request_data=request_data)

    return ck_wrapper


def pack_response(api_func):
    def pr_wrapper(request_data):
        try:
            response = api_func(request_data=request_data)
        except BackendBaseException as e:
            response = {
                'status': e.CODE,
                'error_message': str(e)
            }
        return JsonResponse(data=response,
                            json_dumps_params={'ensure_ascii': False},
                            safe=False)

    return pr_wrapper


# Create your views here.
@require_http_methods(["GET"])
@prepare_request_data
@check_authentication
@pack_response
def login(request_data):
    user = mod_user.User(email=request_data['email'],
                         pswd_hash=request_data['pswd_hash'])
    logged_in_users[user.get_user_id()] = user

    response = {
        'user_id': user.get_user_id(),
        'session_id': user.get_session_id(),
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@prepare_request_data
@check_authentication
@pack_response
def register(request_data):
    user = mod_user.User.new_user(email=request_data['email'],
                                  pswd_hash=request_data['pswd_hash'],
                                  user_name=request_data['user_name'],
                                  gender=request_data['gender'],
                                  resident_city_id=request_data['resident_city_id'])

    response = {
        'user_id': user.get_user_id(),
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@prepare_request_data
@check_authentication
@check_token
@pack_response
def reset_password(request_data):
    user = logged_in_users[request_data['user_id']]
    user.reset_password(old_pswd_hash=request_data['old_pswd_hash'],
                        new_pswd_hash=request_data['new_pswd_hash'])

    response = {
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@prepare_request_data
@check_authentication
@check_token
@pack_response
def get_user_info(request_data):
    user = logged_in_users[request_data['user_id']]
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
@prepare_request_data
@check_authentication
@check_token
@pack_response
def set_user_info(request_data):
    user = logged_in_users[request_data['user_id']]
    user_info = user.get_user_info()

    user.set_email(email=request_data['email'])
    user_info.set_user_name(user_name=request_data['user_name'])
    user_info.set_gender(gender=request_data['gender'])
    user_info.set_resident_city_id(city_id=request_data['resident_city_id'])

    response = {
        'status': 0
    }
    return response


@require_http_methods(["GET"])
@prepare_request_data
@check_authentication
@pack_response
def address_to_city(request_data):
    city = mod_city.get_or_create_city_instance(address=request_data['address'])

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
@prepare_request_data
@check_authentication
@pack_response
def gps_to_city(request_data):
    city = mod_city.get_or_create_city_instance(latitude=request_data['latitude'],
                                                longitude=request_data['longitude'])
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
