"""Api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from Server.settings import DEBUG
from apps.api import views


urlpatterns = []

for view in views.__all__:
    if callable(getattr(views, view)):
        urlpatterns.append(path(rf'{view}/', getattr(views, view), name=view))

if DEBUG:
    urlpatterns.extend([
        path('cities/', views.city_list),
        path('cities/<int:city_id>/', views.city_detail),
        path('users/', views.user_list),
        path('users/<int:user_id>/', views.user_detail),
        path('travel_groups/', views.travel_group_list),
        path('travel_groups/<int:travel_group_id>/', views.travel_group_detail),
        path('travels/', views.travel_list),
        path('travels/<int:travel_id>/', views.travel_detail)
    ])
