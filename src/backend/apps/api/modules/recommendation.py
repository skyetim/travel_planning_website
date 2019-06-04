from datetime import date as ddate

import apps.db.User.models as db_user
import apps.db.Travel.models as db_travel

import apps.api.modules.city as mod_city
import apps.api.modules.travel as mod_travel
import apps.api.modules.user as mod_user

from apps.api.modules.exceptions import *

import math
import numpy as np

# 以下所有user如无意外均指User类的实例对象
def get_time_delta_days(target_date):
    today = ddate.today()
    time_delta = today-ddate(*[int(x) for x in target_date.split("-")])
    time_delta_days = abs(time_delta.days)

def get_rad(theta):
    #将经纬度变换为弧度
    return theta * math.pi/180.0

def get_city_distance(city_id_1,city_id_2):
    # 求两个城市之间的距离
    Earth_Radius = 6378

    city_1 = mod_city.get_city_instance_by_id(city_id_1) #database对象
    rad_Lat_1 = get_rad(city_1.latitutde)
    rad_Lon_1 = get_rad(city_1.longtitude)

    city_2 = mod_city.get_city_instance_by_id(city_id_2) 
    rad_Lat_2 = get_rad(city_2.latitutde)
    rad_Lon_2 = get_rad(city_2.longtitude)

    if rad_Lat_1 < 0: 
        rad_Lat_1 = math.pi / 2 + np.abs(rad_Lat_1) #south  
    if rad_Lat_1 > 0: 
        rad_Lat_1 = math.pi / 2 - np.abs(rad_Lat_1) #north  
    if rad_Lon_1 < 0:  
        rad_Lon_1 = math.pi * 2 - np.abs(rad_Lon_1) #west  
    if rad_Lat_2 < 0:  
        rad_Lat_2 = math.pi / 2 + np.abs(rad_Lat_2) #south  
    if rad_Lat_2 > 0:  
        rad_Lat_2 = math.pi / 2 - np.abs(rad_Lat_2) #north  
    if rad_Lon_2 < 0:
        rad_Lon_2 = math.pi * 2 - np.abs(rad_Lon_2) #west     

    x1 = Earth_Radius * math.cos(rad_Lon_1) * math.sin(rad_Lat_1)
    y1 = Earth_Radius * math.sin(rad_Lon_1) * math.sin(rad_Lat_1)
    z1 = Earth_Radius * math.cos(rad_Lat_1)

    x2 = Earth_Radius * math.cos(rad_Lon_2) * math.sin(rad_Lat_2)
    y2 = Earth_Radius * math.sin(rad_Lon_2) * math.sin(rad_Lat_2)
    z2 = Earth_Radius * math.cos(rad_Lat_2)

    d = math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    theta = math.acos((Earth_Radius**2+Earth_Radius**2-d**2)/(2*Earth_Radius*Earth_Radius))
    dist = theta*Earth_Radius

    return dist

# 实现为同城推荐
def recommend_friend_list(user, amount=10):
    # 从用户数据库中找不是自己好友的那些
    # 根据所在城市、去过的城市等进行匹配推荐（随机抽取）
    # 不要求高精度排序
    # 总数不超过amount
    my_user_id = user.get_user_id()
    my_resident_city = db_user.UserInfo.objects.get(user_id=my_user_id).resident_city_id
    friend_id_list = user.get_friend_list()
    other_user_list = db_user.UserInfo.objects.exclude(user_id=my_user_id)

    user_id_list = []
    for other_user in other_user_list:
        if other_user.user_id not in friend_id_list:
            if other_user.resident_city_id == my_resident_city:
                user_id_list.append(other_user.user_id)

    if len(user_id_list) < amount:
        return user_id_list
    else:
        return user_id_list[:amount]


def recommend_travel_group_list(user, amount=10):
    # 遍历好友的旅行记录
    # 根据时间和今天的距离排序进行推荐
    # 总数不超过amount

    user_id = user.get_user_id()

    friend_list = user.get_friend_list()
    other_travel_group_list = []
    for fr in friend_list:
        for tg_id in user.get_other_travel_group_list(fr):
            travel_group = mod_travel.TravelGroup(
                user_id=user_id, travel_group_id=tg_id)
            travel_list = travel_group.get_travel_list()
            travel = mod_travel.Travel(user_id=user_id,travel_id=travel_list[0])
            company_list = travel.get_company_list() # 得到朋友travel的company，自己不允许出现在里面

            if travel_list == []:
                continue
            if user_id not in company_list:
                rep_time = mod_travel.Travel(
                    user_id=user_id, travel_id=travel_list[0]).get_travel_info().get_date_start()
            # represent time in isoformat
            # e.g. "1989-06-04"

            other_travel_group_list.append(
                {"travel_group_id": tg_id, "time_delta_days": get_time_delta_days(rep_time)})
    other_travel_group_list.sort(key=lambda x: x["time_Delta_days"])
    if len(other_travel_group_list) < amount:
        amount = len(other_travel_group_list)

    recommend_list = []
    for i in range(amount):
        recommend_list.append(other_travel_group_list[i]["travel_group_id"])
    return recommend_list


def recommend_city_list_by_travel(user, travel_id, amount=3):
    # 遍历好友的旅行记录
    # 根据城市和该travel的距离排序进行推荐
    # 不包括本城市
    # 总数不超过amount

    user_id = user.get_user_id()
    travel = mod_travel.Travel(user_id, travel_id) # travel 是Travel类实例对象
    travel_info = travel.get_travel_info()
    my_city = travel_info.get_city_id()
    friend_list = user.get_friend_list() # friend id list

    other_travel_group_list = []
    for fr in friend_list:
        for tg_id in user.get_other_travel_group_list(fr):
            travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
            travel_list = travel_group.get_travel_list()
            if travel_list == []:
                continue
            for travel_id in travel_list:
                travel = mod_travel.Travel(user_id=user_id, travel_id=travel_id)
                company_list = travel.get_company_list()
                if user_id not in company_list:
                    city = travel.get_travel_info().get_city_id()
                    if city != my_city:
                        other_travel_group_list.append(
                            {"city_id":city, "city_distance":get_city_distance(my_city, city)}
                        )

    other_travel_group_list.sort(key=lambda x: x["city_distance"])

    if len(other_travel_group_list) < amount:
        amount = len(other_travel_group_list)

    recommend_list = []

    for i in range(amount):
        recommend_list.append(other_travel_group_list[i]["city_id"])            

    return recommend_list


def recommend_city_list_by_travel_group(user, travel_group_id, amount=3):
    # 遍历好友的旅行记录
    # 根据城市和该travel_group中已有的距离排序进行推荐
    # 不包括该travel_group中已有的city
    # 总数不超过amount

    user_id = user.get_user_id()
    travel_group = mod_travel.TravelGroup(user_id, travel_group_id)
    travel_list = travel_group.get_travel_list()
    my_city_list=[]
    for travel in travel_list:
        travel_info = travel.get_travel_info()
        my_city = travel_info.get_city_id()
        my_city_list.append(my_city)

    friend_list = user.get_friend_list()

    other_travel_group_list = []
    for my_city in my_city_list:
        for fr in friend_list:
            for tg_id in user.get_other_travel_group_list(fr):
                travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
                travel_list = travel_group.get_travel_list()
                if travel_list == []:
                    continue
                for travel_id in travel_list:
                    travel = mod_travel.Travel(user_id=user_id, travel_id=travel_id)
                    company_list = travel.get_company_list()
                    if user_id not in company_list:
                        city = travel.get_travel_info().get_city_id()
                        if city not in my_city_list:
                            other_travel_group_list.append(
                                {"city_id":city, "city_distance":get_city_distance(my_city, city)}
                            )

    other_travel_group_list.sort(key=lambda x: x["city_distance"])

    if len(other_travel_group_list) < amount:
        amount = len(other_travel_group_list)

    recommend_list = []

    for i in range(amount):
        recommend_list.append(other_travel_group_list[i]["city_id"])   

    return recommend_list


def recommend_travel_list_by_travel(user, travel_id, amount=5):
    # 遍历好友的旅行记录
    # 根据城市和该travel的距离、时间间隔排序进行推荐
    # 总数不超过amount

    user_id = user.get_user_id()
    travel = mod_travel.Travel(user_id, travel_id) # travel 是Travel类实例对象
    travel_info = travel.get_travel_info()
    my_city = travel_info.get_city_id()
    friend_list = user.get_friend_list() # friend id list

    other_travel_group_list = []
    for fr in friend_list:
        for tg_id in user.get_other_travel_group_list(fr):
            travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
            travel_list = travel_group.get_travel_list()
            if travel_list == []:
                continue
            #rep_time = mod_travel.Travel(user_id=user_id, travel_id=travel_list[0]).get_travel_info().get_date_start()
            for travel_id in travel_list:
                travel = mod_travel.Travel(user_id=user_id,travel_id=travel_id)
                company_list = travel.get_company_list()
                if user_id not in company_list: 
                    rep_time = travel.get_travel_info().get_date_start()
                    city = travel.get_travel_info().get_city_id()
                    if city != my_city:
                        other_travel_group_list.append(
                            {"travel_id":travel_id, "time_delta_days": get_time_delta_days(rep_time), "city_distance":get_city_distance(my_city, city)}
                    )    
    other_travel_group_list.sort(key=lambda x: np.sqrt((int(x["city_distance"] / 50))**2 + (int(x["time_delta_days"] / 1))**2))

    if len(other_travel_group_list) < amount:
        amount = len(other_travel_group_list)

    recommend_list = []

    for i in range(amount):
        recommend_list.append(other_travel_group_list[i]["travel_id"])   

    return recommend_list


def recommend_travel_list_by_travel_group(user, travel_group_id, amount=5):
    # 遍历好友的旅行记录
    # 根据城市和该travel_group中城市的距离、时间间隔排序进行推荐
    # 总数不超过amount
    user_id = user.get_user_id()
    travel_group = mod_travel.TravelGroup(user_id, travel_group_id)
    travel_list = travel_group.get_travel_list()
    my_city_list=[]
    for travel in travel_list:
        travel_info = travel.get_travel_info()
        my_city = travel_info.get_city_id()
        my_city_list.append(my_city)

    friend_list = user.get_friend_list()

    other_travel_group_list = []
    for my_city in my_city_list:
        for fr in friend_list:
            for tg_id in user.get_other_travel_group_list(fr):
                travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
                travel_list = travel_group.get_travel_list()
                if travel_list == []:
                    continue

                for travel_id in travel_list:                   
                    travel = mod_travel.Travel(user_id=user_id,travel_id=travel_id)
                    company_list = travel.get_company_list()
                    if user_id not in company_list:
                        rep_time = travel.get_travel_info().get_date_start()
                        city = travel.get_travel_info().get_city_id()                     
                        if city not in my_city_list:
                            other_travel_group_list.append(
                                {"travel_id":travel_id, "time_delta_days": get_time_delta_days(rep_time),"city_distance":get_city_distance(my_city, city)}
                            )

    other_travel_group_list.sort(key=lambda x: np.sqrt((int(x["city_distance"] / 50))**2 + (int(x["time_delta_days"] / 1))**2))

    if len(other_travel_group_list) < amount:
        amount = len(other_travel_group_list)

    recommend_list = []

    for i in range(amount):
        recommend_list.append(other_travel_group_list[i]["travel_id"])   

    return recommend_list

