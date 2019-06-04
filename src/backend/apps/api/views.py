from datetime import date, timedelta
from functools import wraps
from typing import Dict, List

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.api.modules import city as mod_city, user as mod_user, travel as mod_travel
from apps.api.modules.exceptions import *
from apps.db.City import models as db_city, serializers as srl_city
from apps.db.Message import models as db_msg
from apps.db.Travel import models as db_travel, serializers as srl_travel
from apps.db.User import models as db_user, serializers as srl_user
from server.settings import DEBUG


__all__: List[str] = []
__all__.extend(['register', 'login', 'logout', 'reset_password'])
__all__.extend(['get_user_info', 'set_user_info', 'set_user_avatar_url'])
__all__.extend(['add_friend', 'remove_friend'])
__all__.extend(['get_friend_list', 'get_friend_info', 'set_friend_note'])
__all__.extend(['get_others_user_info'])
__all__.extend(['get_travel_group_list', 'get_others_travel_group_list'])
__all__.extend(['add_travel_group', 'remove_travel_group',
                'get_all_travel_group_details', 'get_others_all_travel_group_details',
                'get_travel_group_info_list', 'get_others_travel_group_info_list',
                'get_travel_group_details',
                'get_travel_group_info', 'set_travel_group_info'])
__all__.extend(['get_travel_list'])
__all__.extend(['add_travel', 'remove_travel', 'move_travel',
                'get_travel_info_list',
                'get_travel_info', 'set_travel_info'])
__all__.extend(['invite_travel_company', 'join_friends_travel',
                'remove_travel_company'])
__all__.extend(['get_friend_msg_list', 'del_friend_msg',
                'get_travel_msg_list', 'del_travel_msg'])
__all__.extend(['address_to_city', 'address_to_city_list',
                'gps_to_city', 'city_id_to_city'])

REQUEST_METHOD_LIST: List[str] = ['POST']

if DEBUG:
    REQUEST_METHOD_LIST.append('GET')

LOGGED_IN_USERS: Dict[int, mod_user.User] = {}

SESSION_TIMEOUT: timedelta = timedelta(minutes=20)


def prepare_request_data(func):
    @wraps(wrapped=func)
    def prd_wrapper(request):
        def cast(name, cast_func):
            if name in request_data:
                request_data[name] = cast_func(request_data[name])

        request_data = getattr(request, request.method).dict()
        cast(name='user_id', cast_func=int)
        cast(name='friend_user_id', cast_func=int)
        cast(name='other_user_id', cast_func=int)
        cast(name='email', cast_func=str.lower)
        cast(name='pswd_hash', cast_func=str.upper)
        cast(name='old_pswd_hash', cast_func=str.upper)
        cast(name='new_pswd_hash', cast_func=str.upper)
        cast(name='city_id', cast_func=int)
        cast(name='resident_city_id', cast_func=int)
        cast(name='latitude', cast_func=float)
        cast(name='longitude', cast_func=float)
        cast(name='travel_group_id', cast_func=int)
        cast(name='other_travel_group_id', cast_func=int)
        cast(name='travel_group_color', cast_func=str.upper)
        cast(name='travel_id', cast_func=int)
        cast(name='date_start', cast_func=lambda date_string: date(*map(int, date_string.split('-'))))
        cast(name='date_end', cast_func=lambda date_string: date(*map(int, date_string.split('-'))))

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
    def ct_wrapper(request_data):
        user_id = request_data['user_id']
        session_id = request_data['session_id']
        if user_id not in LOGGED_IN_USERS:
            raise UserAuthorizationException(f'User (ID={user_id}) does not log in.')
        try:
            user_session = db_user.UserSession.objects.get(user_id=user_id,
                                                           session_id=session_id)
        except db_user.UserSession.DoesNotExist:
            del LOGGED_IN_USERS[user_id]
            db_user.UserSession.objects.filter(user_id=user_id).delete()
            raise UserAuthorizationException(f'User (ID={user_id}) and session (ID={session_id})'
                                             f' do not match, log out.')
        else:
            if user_session.last_action_time < timezone.now() - SESSION_TIMEOUT:
                del LOGGED_IN_USERS[user_id]
                db_user.UserSession.objects.filter(user_id=user_id).delete()
                raise UserSessionTimeoutException(f'User (ID={user_id}) has no action for 10 minutes, log out.')
            user_session.save()
            return func(request_data=request_data)

    return ct_wrapper


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

        wrapped_func = check_authentication(func=api_func)
        if check_tokens:
            wrapped_func = check_token(func=wrapped_func)
        wrapped_func = pack_response(func=wrapped_func)
        wrapped_func = prepare_request_data(func=wrapped_func)
        wrapped_func = api_view(http_method_names=REQUEST_METHOD_LIST)(func=wrapped_func)
        wrapped_func = require_http_methods(request_method_list=REQUEST_METHOD_LIST)(func=wrapped_func)

        return wrapped_func

    return decorator


# Create your views here.
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


@api(check_tokens=False)
def login(request_data):
    user = mod_user.User(email=request_data['email'],
                         pswd_hash=request_data['pswd_hash'])
    LOGGED_IN_USERS[user.get_user_id()] = user

    response = {
        'user_id': user.get_user_id(),
        'session_id': user.get_session_id()
    }
    return response


@api(check_tokens=True)
def logout(request_data):
    try:
        del LOGGED_IN_USERS[request_data['user_id']]
    except KeyError:
        pass
    db_user.UserSession.objects.filter(user_id=request_data['user_id']).delete()

    response = {}
    return response


@api(check_tokens=True)
def reset_password(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    user.reset_password(old_pswd_hash=request_data['old_pswd_hash'],
                        new_pswd_hash=request_data['new_pswd_hash'])

    response = {}
    return response


@api(check_tokens=True)
def get_user_info(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    user_info = user.get_user_info()

    response = dict(user)
    response.update(dict(user_info))
    return response


@api(check_tokens=True)
def set_user_info(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    user_info = user.get_user_info()

    user.set_email(email=request_data['email'])
    user_info.set_user_name(user_name=request_data['user_name'])
    user_info.set_gender(gender=request_data['gender'])
    user_info.set_resident_city_id(city_id=request_data['resident_city_id'])
    user_info.set_comment(comment=request_data['comment'])

    response = {}
    return response


@api(check_tokens=True)
def set_user_avatar_url(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    user_info = user.get_user_info()

    user_info.set_avatar_url(avatar_url=request_data['avatar_url'])

    response = {}
    return response


@api(check_tokens=True)
def add_friend(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    user.add_friend(friend_user_id=request_data['friend_user_id'],
                    friend_note=request_data['friend_note'])

    response = {}
    return response


@api(check_tokens=True)
def remove_friend(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    user.remove_friend(friend_user_id=request_data['friend_user_id'])

    response = {}
    return response


@api(check_tokens=True)
def get_friend_list(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    friend_list = user.get_friend_list()

    response = {
        'count': len(friend_list),
        'friend_list': friend_list
    }
    return response


@api(check_tokens=True)
def get_friend_info(request_data):
    friend_user_info = mod_user.FriendInfo(user_id=request_data['user_id'],
                                           friend_user_id=request_data['friend_user_id'])

    response = dict(friend_user_info)
    return response


@api(check_tokens=True)
def set_friend_note(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    user.set_friend_note(friend_user_id=request_data['friend_user_id'],
                         friend_note=request_data['friend_note'])

    response = {}
    return response


@api(check_tokens=True)
def get_others_user_info(request_data):
    user_id = request_data['user_id']
    other_user_id = request_data['other_user_id ']
    is_friend = mod_user.is_friend(user_id=user_id, friend_user_id=other_user_id)

    if other_user_id == user_id:
        user = LOGGED_IN_USERS[request_data['user_id']]
        other_user_info = user.get_user_info()
    elif is_friend:
        other_user_info = mod_user.FriendInfo(user_id=user_id, friend_user_id=other_user_id)
    else:
        other_user_info = mod_user.UserInfoBase(user_id=other_user_id)

    response = dict(other_user_info)
    response['is_friend'] = is_friend
    return response


@api(check_tokens=True)
def get_travel_group_list(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    travel_group_list = user.get_travel_group_list()

    response = {
        'count': len(travel_group_list),
        'travel_group_list': travel_group_list
    }
    return response


@api(check_tokens=True)
def get_others_travel_group_list(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    others_travel_group_list = user.get_others_travel_group_list(other_user_id=request_data['other_user_id'])

    response = {
        'count': len(others_travel_group_list),
        'travel_group_list': others_travel_group_list
    }
    return response


@api(check_tokens=True)
def add_travel_group(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    travel_group = user.add_travel_group(travel_group_name=request_data['travel_group_name'],
                                         travel_group_note=request_data['travel_group_note'],
                                         travel_group_color=request_data['travel_group_color'])

    response = {
        'travel_group_id': travel_group.get_travel_group_id()
    }
    return response


@api(check_tokens=True)
def remove_travel_group(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    user.remove_travel_group(travel_group_id=request_data['travel_group_id'])

    response = {}
    return response


@api(check_tokens=True)
def get_all_travel_group_details(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    travel_group_list = [mod_travel.TravelGroup(user_id=user.get_user_id(),
                                                travel_group_id=travel_group_id)
                         for travel_group_id in user.get_travel_group_list()]

    response = {
        'count': len(travel_group_list),
        'travel_group_info_list': [travel_group.get_travel_group_detail()
                                   for travel_group in travel_group_list]
    }
    return response


@api(check_tokens=True)
def get_others_all_travel_group_details(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]

    others_travel_group_list = user.get_others_travel_group_list(other_user_id=request_data['other_user_id'])
    travel_group_list = [mod_travel.TravelGroup(user_id=user.get_user_id(),
                                                travel_group_id=travel_group_id)
                         for travel_group_id in others_travel_group_list]
    response = {
        'count': len(travel_group_list),
        'travel_group_info_list': [travel_group.get_travel_group_detail()
                                   for travel_group in travel_group_list]
    }
    return response


@api(check_tokens=True)
def get_travel_group_info_list(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    travel_group_list = user.get_travel_group_list()

    response = {
        'count': len(travel_group_list),
        'travel_group_info_list': [dict(mod_travel.TravelGroup(user_id=user.get_user_id(),
                                                               travel_group_id=travel_group_id))
                                   for travel_group_id in travel_group_list]
    }
    return response


@api(check_tokens=True)
def get_others_travel_group_info_list(request_data):
    user = LOGGED_IN_USERS[request_data['user_id']]
    others_travel_group_list = user.get_others_travel_group_list(other_user_id=request_data['other_user_id'])

    response = {
        'count': len(others_travel_group_list),
        'travel_group_info_list': [dict(mod_travel.TravelGroup(user_id=user.get_user_id(),
                                                               travel_group_id=travel_group_id))
                                   for travel_group_id in others_travel_group_list]
    }
    return response


@api(check_tokens=True)
def get_travel_group_details(request_data):
    travel_group = mod_travel.TravelGroup(user_id=request_data['user_id'],
                                          travel_group_id=request_data['travel_group_id'])

    response = travel_group.get_travel_group_detail()
    return response


@api(check_tokens=True)
def get_travel_group_info(request_data):
    travel_group = mod_travel.TravelGroup(user_id=request_data['user_id'],
                                          travel_group_id=request_data['travel_group_id'])

    response = dict(travel_group)
    return response


@api(check_tokens=True)
def set_travel_group_info(request_data):
    travel_group = mod_travel.TravelGroup(user_id=request_data['user_id'],
                                          travel_group_id=request_data['travel_group_id'])

    travel_group.set_travel_group_name(name=request_data['travel_group_name'])
    travel_group.set_travel_group_note(note=request_data['travel_group_note'])
    travel_group.set_travel_group_color(color=request_data['travel_group_color'])

    response = {}
    return response


@api(check_tokens=True)
def get_travel_list(request_data):
    travel_group = mod_travel.TravelGroup(user_id=request_data['user_id'],
                                          travel_group_id=request_data['travel_group_id'])

    travel_list = travel_group.get_travel_list()

    response = {
        'count': len(travel_list),
        'travel_list': travel_list
    }
    return response


@api(check_tokens=True)
def add_travel(request_data):
    travel_group = mod_travel.TravelGroup(user_id=request_data['user_id'],
                                          travel_group_id=request_data['travel_group_id'])

    travel = travel_group.add_travel(date_start=request_data['date_start'],
                                     date_end=request_data['date_end'],
                                     city_id=request_data['city_id'],
                                     travel_note=request_data['travel_note'],
                                     visibility=request_data['visibility'])

    response = {
        'travel_id': travel.get_travel_id()
    }
    return response


@api(check_tokens=True)
def remove_travel(request_data):
    travel_group = mod_travel.TravelGroup(user_id=request_data['user_id'],
                                          travel_group_id=request_data['travel_group_id'])

    travel_group.remove_travel(travel_id=request_data['travel_id'])

    response = {}
    return response


@api(check_tokens=True)
def move_travel(request_data):
    travel_group = mod_travel.TravelGroup(user_id=request_data['user_id'],
                                          travel_group_id=request_data['travel_group_id'])

    travel_group.move_travel_to_other_group(travel_id=request_data['travel_id'],
                                            other_travel_group_id=request_data['other_travel_group_id'])

    response = {}
    return response


@api(check_tokens=True)
def get_travel_info_list(request_data):
    user_id = request_data['user_id']

    travel_group = mod_travel.TravelGroup(user_id=user_id,
                                          travel_group_id=request_data['travel_group_id'])

    travel_list = travel_group.get_travel_list()

    response = {
        'count': len(travel_list),
        'travel_info_list': [dict(mod_travel.TravelInfo(user_id=user_id,
                                                        travel_id=travel_id))
                             for travel_id in travel_list]
    }
    return response


@api(check_tokens=True)
def get_travel_info(request_data):
    travel_info = mod_travel.TravelInfo(user_id=request_data['user_id'],
                                        travel_id=request_data['travel_id'])

    response = dict(travel_info)
    return response


@api(check_tokens=True)
def set_travel_info(request_data):
    travel_info = mod_travel.TravelInfo(user_id=request_data['user_id'],
                                        travel_id=request_data['travel_id'])

    travel_info.set_date_start(date_start=request_data['date_start'])
    travel_info.set_date_end(date_end=request_data['date_end'])
    travel_info.set_city_id(city_id=request_data['city_id'])
    travel_info.set_travel_note(note=request_data['travel_note'])
    travel_info.set_visibility(visibility=request_data['visibility'])

    response = {}
    return response


@api(check_tokens=True)
def invite_travel_company(request_data):
    travel = mod_travel.Travel(user_id=request_data['user_id'],
                               travel_id=request_data['travel_id'])

    travel.invite_company(company_user_id=request_data['friend_user_id'])

    response = {}
    return response


@api(check_tokens=True)
def join_friends_travel(request_data):
    travel = mod_travel.Travel(user_id=request_data['friend_user_id'],
                               travel_id=request_data['friend_travel_id'])

    travel.add_company(company_user_id=request_data['user_id'])

    response = {}
    return response


@api(check_tokens=True)
def remove_travel_company(request_data):
    travel = mod_travel.Travel(user_id=request_data['user_id'],
                               travel_id=request_data['travel_id'])

    travel.remove_company(company_user_id=request_data['friend_user_id'])

    response = {}
    return response


@api(check_tokens=False)
def get_friend_msg_list(request_data):
    friend_msg_list = db_msg.FriendRequest.objects.filter(user_id=request_data['user_id'])

    response = {
        'count': len(friend_msg_list),
        'msg_list': list(map(dict, friend_msg_list))
    }
    return response


@api(check_tokens=False)
def del_friend_msg(request_data):
    db_msg.FriendRequest.objects.filter(user_id=request_data['user_id'],
                                        msg_id=request_data['msg_id'])

    response = {}
    return response


@api(check_tokens=False)
def get_travel_msg_list(request_data):
    travel_msg_list = db_msg.TravelAssociation.objects.filter(user_id=request_data['user_id'])

    response = {
        'count': len(travel_msg_list),
        'msg_list': list(map(dict, travel_msg_list))
    }
    return response


@api(check_tokens=False)
def del_travel_msg(request_data):
    db_msg.TravelAssociation.objects.filter(user_id=request_data['user_id'],
                                            msg_id=request_data['msg_id'])

    response = {}
    return response


@api(check_tokens=False)
def address_to_city(request_data):
    city = mod_city.get_city_instance_by_address(address=request_data['address'])

    response = dict(city)
    return response


@api(check_tokens=False)
def address_to_city_list(request_data):
    city_list = mod_city.get_city_instance_list_by_address(address=request_data['address'])

    response = {
        'count': len(city_list),
        'city_list': list(map(dict, city_list))
    }
    return response


@api(check_tokens=False)
def gps_to_city(request_data):
    city = mod_city.get_city_instance_by_gps(latitude=request_data['latitude'],
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
        raise TravelGroupDoesNotExistException(f'Travel group (ID={travel_group_id}) does not exist.')

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
