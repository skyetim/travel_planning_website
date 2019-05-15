from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

import apps.api.modules.city as city_mod
import apps.api.modules.user as user_mod
from apps.api.modules.exceptions import BackendBaseException


__all__ = ['login', 'register', 'address_to_city']


# Create your views here.
@require_http_methods(["GET"])
def login(request):
    response = {}
    try:
        user = user_mod.User(email=request.GET.get('email'),
                             pswd_hash=request.GET.get('pswd_hash'))
        response['user_id'] = user.get_user_id()
        response['status'] = 0
    except BackendBaseException as e:
        response['status'] = e.CODE
        response['error_message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["GET"])
def register(request):
    response = {}
    try:
        user = user_mod.User.new_user(email=request.GET.get('email'),
                                      pswd_hash=request.GET.get('pswd_hash'),
                                      gender=request.GET.get('gender'),
                                      resident_city_id=int(request.GET.get('resident_city_id')))
        response['user_id'] = user.get_user_id()
        response['status'] = 0
    except BackendBaseException as e:
        response['status'] = e.CODE
        response['error_message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["GET"])
def address_to_city(request):
    city = city_mod.address_to_city_instance(address=request.GET.get('address'))
    response = {
        'city_id': city.city_id,
        'country_name': city.country_name,
        'province_name': city.province_name,
        'city_name': city.city_name,
        'status': 0
    }
    return JsonResponse(response)
