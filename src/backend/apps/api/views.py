from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

import apps.api.modules.city as mod_city
import apps.api.modules.user as mod_user
import apps.db.User.models as db_user
from apps.api.modules.exceptions import *


__all__ = ['login', 'register', 'reset_password', 'address_to_city']

logged_in_users = {}


def check_authorization(request):
    pass


def check_token(request):
    try:
        user_session = db_user.UserSession.objects.get(user_id=request.GET.get('user_id'),
                                                       session_id=request.GET.get('session_id'))
    except ObjectDoesNotExist:
        db_user.UserSession.objects.filter(user_id=request.GET.get('user_id')).delete()
        raise UserAuthorizationException('Authorization error.')


# Create your views here.
@require_http_methods(["GET"])
def login(request):
    check_authorization(request=request)

    response = {}
    try:
        user = mod_user.User(email=request.GET.get('email'),
                             pswd_hash=request.GET.get('pswd_hash'))
        response['user_id'] = user.get_user_id()
        response['session_id'] = user.get_session_id()
        response['status'] = 0
        logged_in_users[user.get_user_id()] = user
    except BackendBaseException as e:
        response['status'] = e.CODE
        response['error_message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["GET"])
def register(request):
    check_authorization(request=request)

    response = {}
    try:
        user = mod_user.User.new_user(email=request.GET.get('email'),
                                      pswd_hash=request.GET.get('pswd_hash'),
                                      user_name=request.GET.get('user_name'),
                                      gender=request.GET.get('gender'),
                                      resident_city_id=int(request.GET.get('resident_city_id')))
        response['user_id'] = user.get_user_id()
        response['status'] = 0
    except BackendBaseException as e:
        response['status'] = e.CODE
        response['error_message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["GET"])
def reset_password(request):
    check_authorization(request=request)
    check_token(request=request)

    response = {}
    try:
        user = logged_in_users[request.GET.get('user_id')]
        user.reset_password(old_pswd_hash=request.GET.get('old_pswd_hash'),
                            new_pswd_hash=request.GET.get('new_pswd_hash'))
    except BackendBaseException as e:
        response['status'] = e.CODE
        response['error_message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["GET"])
def address_to_city(request):
    city = mod_city.address_to_city_instance(address=request.GET.get('address'))
    response = {
        'city_id': city.city_id,
        'country_name': city.country_name,
        'province_name': city.province_name,
        'city_name': city.city_name,
        'status': 0
    }
    return JsonResponse(response)
