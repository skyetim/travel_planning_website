from django.http import HttpResponse


def site_home(request):
    return HttpResponse('Site Home Page')


def login(request):
    return HttpResponse('Login Page')


def user_home(request):
    return HttpResponse('User Home Page')
