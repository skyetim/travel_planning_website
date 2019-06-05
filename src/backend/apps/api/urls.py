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

from apps.api import views
from server.settings import DEBUG


urlpatterns = []

for view in views.__all__:
    if callable(getattr(views, view)):
        urlpatterns.extend([
            path(route=view, view=getattr(views, view), name=view),
            path(route=f'{view}/', view=getattr(views, view), name=view)
        ])

if DEBUG:
    route_view = {
        'cities': views.city_list,
        'cities/<int:city_id>': views.city_detail,
        'users': views.user_list,
        'users/<int:user_id>': views.user_detail,
        'travel_groups': views.travel_group_list,
        'travel_groups/<int:travel_group_id>': views.travel_group_detail,
        'travels': views.travel_list,
        'travels/<int:travel_id>': views.travel_detail,
        'friend_messages': views.friend_message_list,
        'friend_messages/<int:msg_id>': views.friend_message_detail,
        'travel_messages': views.travel_message_list,
        'travel_messages/<int:msg_id>': views.travel_message_detail
    }
    for route, view in route_view.items():
        urlpatterns.extend([
            path(route=route, view=view),
            path(route=f'{route}/', view=view)
        ])
