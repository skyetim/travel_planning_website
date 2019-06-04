from django.http import HttpResponse


def backend_home(request):
    return HttpResponse('Backend Home Page')
