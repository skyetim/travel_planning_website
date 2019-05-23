from datetime import timedelta
from functools import wraps

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

import apps.api.modules.city as mod_city
import apps.api.modules.user as mod_user
import apps.db.City.models as db_city
import apps.db.City.serializers as srl_city
import apps.db.Travel.models as db_travel
import apps.db.Travel.serializers as srl_travel
import apps.db.User.models as db_user
import apps.db.User.serializers as srl_user
from apps.api.modules.exceptions import *


__all__ = []
__all__.extend(['login', 'register', 'reset_password'])
__all__.extend(['get_user_info', 'set_user_info'])
__all__.extend(['address_to_city', 'gps_to_city', 'city_id_to_city'])

request_method_list = ['GET', 'POST']

logged_in_users = {}

SESSION_TIMEOUT = timedelta(minutes=10)


def prepare_request_data(func):
    @wraps(wrapped=func)
    def prd_wrapper(request):
        def cast(name, cast_func):
            if name in request_data:
                request_data[name] = cast_func(request_data[name])

        request_data = getattr(request, request.method).dict()
        cast(name='user_id', cast_func=int)
        cast(name='email', cast_func=str.lower)
        cast(name='pswd_hash', cast_func=str.upper)
        cast(name='old_pswd_hash', cast_func=str.upper)
        cast(name='new_pswd_hash', cast_func=str.upper)
        cast(name='city_id', cast_func=int)
        cast(name='resident_city_id', cast_func=int)
        cast(name='latitude', cast_func=float)
        cast(name='longitude', cast_func=float)

        return func(request_data=request_data)

    return prd_wrapper


def check_authentication(func):
    @wraps(wrapped=func)
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
        #     raise AuthenticationException

        return func(request_data=request_data)

    return ca_wrapper


def check_token(func):
    @wraps(wrapped=func)
    def ck_wrapper(request_data):
        user_id = request_data['user_id']
        session_id = request_data['session_id']
        if user_id not in logged_in_users:
            raise UserAuthorizationException(f'User (ID={user_id}) does not log in.')
        try:
            user_session = db_user.UserSession.objects.get(user_id=user_id,
                                                           session_id=session_id)
        except db_user.UserSession.DoesNotExist:
            db_user.UserSession.objects.filter(user_id=user_id).delete()
            del logged_in_users[user_id]
            raise UserAuthorizationException(f'User (ID={user_id}) and session (ID={session_id}) do not match, log out.')
        else:
            if user_session.last_action_time < timezone.now() - SESSION_TIMEOUT:
                del logged_in_users[user_id]
                raise UserSessionTimeoutException(f'User (ID={user_id}) has no action for 10 minutes, log out.')
            user_session.save()
            return func(request_data=request_data)

    return ck_wrapper


def pack_response(func):
    @wraps(wrapped=func)
    def pr_wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.setdefault('status', 0)
        except BackendBaseException as e:
            response = {
                'status': e.CODE,
                'error_message': str(e)
            }
        return Response(data=response)

    return pr_wrapper


def api(check_tokens):
    def decorator(api_func):

        wrapped_func = pack_response(func=api_func)
        wrapped_func = check_authentication(func=wrapped_func)
        if check_tokens:
            wrapped_func = check_token(wrapped_func)
        wrapped_func = prepare_request_data(func=wrapped_func)
        wrapped_func = api_view(http_method_names=request_method_list)(func=wrapped_func)
        wrapped_func = require_http_methods(request_method_list=request_method_list)(func=wrapped_func)

        return wrapped_func

    return decorator


# Create your views here.
@api(check_tokens=False)
def login(request_data):
    user = mod_user.User(email=request_data['email'],
                         pswd_hash=request_data['pswd_hash'])
    logged_in_users[user.get_user_id()] = user

    response = {
        'user_id': user.get_user_id(),
        'session_id': user.get_session_id()
    }
    return response


@api(check_tokens=False)
def register(request_data):
    user = mod_user.User.new_user(email=request_data['email'],
                                  pswd_hash=request_data['pswd_hash'],
                                  user_name=request_data['user_name'],
                                  gender=request_data['gender'],
                                  resident_city_id=request_data['resident_city_id'])

    response = {
        'user_id': user.get_user_id()
    }
    return response


@api(check_tokens=True)
def reset_password(request_data):
    user = logged_in_users[request_data['user_id']]
    user.reset_password(old_pswd_hash=request_data['old_pswd_hash'],
                        new_pswd_hash=request_data['new_pswd_hash'])

    response = {}
    return response


@api(check_tokens=True)
def get_user_info(request_data):
    user = logged_in_users[request_data['user_id']]
    user_info = user.get_user_info()

    response = dict(user)
    response.update(dict(user_info))
    return response


@api(check_tokens=True)
def set_user_info(request_data):
    user = logged_in_users[request_data['user_id']]
    user_info = user.get_user_info()

    user.set_email(email=request_data['email'])
    user_info.set_user_name(user_name=request_data['user_name'])
    user_info.set_gender(gender=request_data['gender'])
    user_info.set_resident_city_id(city_id=request_data['resident_city_id'])

    response = {}
    return response


@api(check_tokens=False)
def address_to_city(request_data):
    city = mod_city.get_or_create_city_instance(address=request_data['address'])

    response = dict(city)
    return response


@api(check_tokens=False)
def gps_to_city(request_data):
    city = mod_city.get_or_create_city_instance(latitude=request_data['latitude'],
                                                longitude=request_data['longitude'])

    response = dict(city)
    return response


@api(check_tokens=False)
def city_id_to_city(request_data):
    city = mod_city.get_city_instance_by_id(city_id=request_data['city_id'])

    response = dict(city)
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def city_list(request):
    """
    List all cities.
    """

    cities = db_city.City.objects.all()
    serializer = srl_city.CitySerializer(cities, many=True)
    response = {
        'count': len(serializer.data),
        'city_list': serializer.data
    }
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def city_detail(request, city_id):
    """
    Retrieve a city.
    """
    try:
        city = db_city.City.objects.get(city_id=city_id)
    except db_city.City.DoesNotExist:
        raise CityIdDoesNotExistException(f'City (ID={city_id}) does not exist.')

    serializer = srl_city.CitySerializer(city)
    response = serializer.data
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def user_list(request):
    """
    List all users.
    """

    users = db_user.User.objects.all()
    serializer = srl_user.UserSerializer(users, many=True)
    response = {
        'count': len(serializer.data),
        'user_list': serializer.data
    }
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def user_detail(request, user_id):
    """
    Retrieve a user.
    """
    try:
        user = db_user.User.objects.get(user_id=user_id)
    except db_user.User.DoesNotExist:
        raise UserDoesNotExistException(f'User (ID={user_id}) does not exist.')

    serializer = srl_user.UserSerializer(user)
    response = serializer.data
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def travel_group_list(request):
    """
    List all travel groups.
    """

    travel_groups = db_travel.TravelGroup.objects.all()
    serializer = srl_travel.TravelGroupSerializer(travel_groups, many=True)
    response = {
        'count': len(serializer.data),
        'travel_group_list': serializer.data
    }
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def travel_group_detail(request, travel_group_id):
    """
    Retrieve a travel group.
    """
    try:
        travel_group = db_travel.TravelGroup.objects.get(travel_group_id=travel_group_id)
    except db_travel.TravelGroup.DoesNotExist:
        raise TravelGroupDoseNotExistException(f'Travel group (ID={travel_group_id}) does not exist.')

    serializer = srl_travel.TravelGroupSerializer(travel_group)
    response = serializer.data
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def travel_list(request):
    """
    List all travels.
    """

    travels = db_travel.Travel.objects.all()
    serializer = srl_travel.TravelSerializer(travels, many=True)
    response = {
        'count': len(serializer.data),
        'travel_list': serializer.data
    }
    return response


@csrf_exempt
@api_view(http_method_names=['GET'])
@require_http_methods(request_method_list=['GET'])
@pack_response
def travel_detail(request, travel_id):
    """
    Retrieve a travel.
    """
    try:
        travel = db_travel.Travel.objects.get(travel_id=travel_id)
    except db_travel.Travel.DoesNotExist:
        raise TravelDoesNotExistException(f'Travel (ID={travel_id}) does not exist.')

    serializer = srl_travel.TravelSerializer(travel)
    response = serializer.data
    return response
