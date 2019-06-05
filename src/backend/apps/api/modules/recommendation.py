import datetime
import math
from functools import reduce
from random import shuffle as shuffle

import apps.api.modules.city as mod_city
import apps.api.modules.travel as mod_travel
import apps.db.User.models as db_user


# 以下所有user如无意外均指User类的实例对象
def get_time_delta_days(target_date):
    today = datetime.date.today()
    time_delta = today - datetime.date(*[int(x) for x in target_date.split('-')])
    time_delta_days = abs(time_delta.days)
    return time_delta_days


def get_city_distance(city_id_1, city_id_2):
    def cosine_similarity(city_id_1, city_id_2):
        sin = lambda theta: math.sin(theta * math.pi / 180.0)
        cos = lambda theta: math.cos(theta * math.pi / 180.0)

        city_1 = mod_city.get_city_instance_by_id(city_id_1)
        city_2 = mod_city.get_city_instance_by_id(city_id_2)

        return sin(city_1.latitude) * sin(city_2.latitude) \
               + cos(city_1.latitude) * cos(city_2.latitude) \
               * cos(city_2.longitude - city_1.longitude)

    # 求两个城市之间的距离
    Earth_Radius = 6378

    theta = math.acos(cosine_similarity(city_id_1=city_id_1, city_id_2=city_id_2))
    dist = Earth_Radius * theta

    return dist


def make_list_distinct(target_list):
    #去除重复元素且保持顺序不变
    def func(x, y): return x if y in x else x + [y]
    return reduce(func, [[], ] + target_list)


def generate_rec_list(target_list, amount, key):
    #生成适当数量的无重复列表
    recommend_list = []
    for x in target_list:
        recommend_list.append(x[key])
    recommend_list=make_list_distinct(recommend_list)

    if len(recommend_list) < amount:
        amount = len(recommend_list)
    return recommend_list[:amount]

# 实现为同城推荐


def recommend_friend_list(user, amount=10):
    # 从用户数据库中找不是自己好友的那些
    # 根据所在城市、去过的城市等进行匹配推荐（随机抽取）
    # 不要求高精度排序
    # 总数不超过amount
    my_user_id = user.get_user_id()
    my_resident_city = db_user.UserInfo.objects.get(
        user_id=my_user_id).resident_city_id
    friend_id_list = user.get_friend_list()
    other_user_list = db_user.UserInfo.objects.exclude(user_id=my_user_id)

    user_id_list = []
    for other_user in other_user_list:
        if other_user.user_id not in friend_id_list:
            if other_user.resident_city_id == my_resident_city:
                user_id_list.append(other_user.user_id.user_id)
    shuffle(user_id_list)
    user_id_list_1 = make_list_distinct(user_id_list)

    if len(user_id_list_1) >= amount:
        return user_id_list_1[:amount]

    # 若同城用户不足就开始随机推荐
    user_id_list_2 = []
    amount = amount-len(user_id_list_1)
    for other_user in other_user_list:
        if other_user.user_id not in friend_id_list:
            if other_user.resident_city_id != my_resident_city:
                user_id_list_2.append(other_user.user_id.user_id)

    user_id_list_2 = make_list_distinct(user_id_list_2)
    shuffle(user_id_list_2)
    if len(user_id_list_2) > amount:
        user_id_list_2 = user_id_list_2[:amount]

    return user_id_list_1+user_id_list_2


def recommend_travel_group_list(user, amount=10):
    # 遍历好友的旅行记录
    # 根据时间和今天的距离排序进行推荐
    # 总数不超过amount

    user_id = user.get_user_id()

    friend_list = user.get_friend_list()
    other_travel_group_list = []
    for fr in friend_list:
        for tg_id in user.get_others_travel_group_list(fr):
            travel_group = mod_travel.TravelGroup(
                    user_id=user_id, travel_group_id=tg_id)
            travel_list = travel_group.get_travel_list()
            if len(travel_list) == 0:
                continue
            travel = mod_travel.Travel(user_id=user_id, travel_id=travel_list[0])
            company_list = travel.get_company_list()  # 得到朋友travel的company，自己不允许出现在里面
            
            if user_id not in company_list:
                rep_time = travel.get_travel_info().get_date_start()
            # represent time in isoformat
            # e.g. "1989-06-04"

                other_travel_group_list.append({
                    'travel_group_id': tg_id,
                    'time_delta_days': get_time_delta_days(rep_time)
                 })
    other_travel_group_list.sort(key=lambda x: x['time_delta_days'])

    return generate_rec_list(other_travel_group_list, amount, key="travel_group_id")


def recommend_city_list_by_travel(user, travel_id, amount=3):
    # 遍历好友的旅行记录
    # 根据城市和该travel的距离排序进行推荐
    # 不包括本城市
    # 总数不超过amount

    user_id = user.get_user_id()
    travel = mod_travel.Travel(user_id, travel_id)  # travel 是Travel类实例对象
    travel_info = travel.get_travel_info()
    my_city = travel_info.get_city_id()
    friend_list = user.get_friend_list()  # friend id list

    other_travel_group_list = []
    for fr in friend_list:
        for tg_id in user.get_others_travel_group_list(fr):
            travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
            for travel_id in travel_group.get_travel_list():
                travel = mod_travel.Travel(user_id=user_id, travel_id=travel_id)
                company_list = travel.get_company_list()
                if user_id not in company_list:
                    city = travel.get_travel_info().get_city_id()
                    if city != my_city:
                        other_travel_group_list.append({
                            'city_id': city,
                            'city_distance': get_city_distance(my_city, city)
                        })

    other_travel_group_list.sort(key=lambda x: x['city_distance'])

    return generate_rec_list(other_travel_group_list, amount, key="city_id")


def recommend_city_list_by_travel_group(user, travel_group_id, amount=3):
    # 遍历好友的旅行记录
    # 根据城市和该travel_group中已有的距离排序进行推荐
    # 不包括该travel_group中已有的city
    # 总数不超过amount

    user_id = user.get_user_id()
    travel_group = mod_travel.TravelGroup(user_id, travel_group_id)
    my_city_list = []
    for travel_id in travel_group.get_travel_list():
        travel_info = mod_travel.Travel(
                user_id=user_id, travel_id=travel_id).get_travel_info()
        my_city = travel_info.get_city_id()
        my_city_list.append(my_city)

    friend_list = user.get_friend_list()

    other_travel_group_list = []
    for my_city in my_city_list:
        for fr in friend_list:
            for tg_id in user.get_others_travel_group_list(fr):
                travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
                for travel_id in travel_group.get_travel_list():
                    travel = mod_travel.Travel(user_id=user_id, travel_id=travel_id)
                    company_list = travel.get_company_list()
                    if user_id not in company_list:
                        city = travel.get_travel_info().get_city_id()
                        if city not in my_city_list:
                            other_travel_group_list.append({
                                'city_id': city,
                                'city_distance': get_city_distance(my_city, city)
                            })

    other_travel_group_list.sort(key=lambda x: x['city_distance'])

    return generate_rec_list(other_travel_group_list, amount, key="city_id")


def recommend_travel_list_by_travel(user, travel_id, amount=5):
    # 遍历好友的旅行记录
    # 根据城市和该travel的距离、时间间隔排序进行推荐
    # 总数不超过amount

    user_id = user.get_user_id()
    travel = mod_travel.Travel(user_id, travel_id)  # travel 是Travel类实例对象
    travel_info = travel.get_travel_info()
    my_city = travel_info.get_city_id()
    friend_list = user.get_friend_list()  # friend id list

    other_travel_group_list = []
    for fr in friend_list:
        for tg_id in user.get_others_travel_group_list(fr):
            travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
            # rep_time = mod_travel.Travel(user_id=user_id, travel_id=travel_list[0]).get_travel_info().get_date_start()
            for travel_id in travel_group.get_travel_list():
                travel = mod_travel.Travel(user_id=user_id, travel_id=travel_id)
                company_list = travel.get_company_list()
                if user_id not in company_list:
                    rep_time = travel.get_travel_info().get_date_start()
                    city = travel.get_travel_info().get_city_id()
                    if city != my_city:
                        other_travel_group_list.append({
                            "travel_id": travel_id,
                            "time_delta_days": get_time_delta_days(rep_time),
                            "city_distance": get_city_distance(my_city, city)
                        })
    other_travel_group_list.sort(key=lambda x: ((int(x['city_distance'] / 50)) ** 2 + (int(x['time_delta_days'] / 1)) ** 2))

    return generate_rec_list(other_travel_group_list, amount, key="travel_id")


def recommend_travel_list_by_travel_group(user, travel_group_id, amount=5):
    # 遍历好友的旅行记录
    # 根据城市和该travel_group中城市的距离、时间间隔排序进行推荐
    # 总数不超过amount
    user_id = user.get_user_id()
    travel_group = mod_travel.TravelGroup(user_id, travel_group_id)
    my_city_list = []
    for travel_id in travel_group.get_travel_list():
        travel_info = mod_travel.Travel(user_id=user_id,travel_id=travel_id).get_travel_info()
        my_city = travel_info.get_city_id()
        my_city_list.append(my_city)

    friend_list = user.get_friend_list()

    other_travel_group_list = []
    for my_city in my_city_list:
        for fr in friend_list:
            for tg_id in user.get_others_travel_group_list(fr):
                travel_group = mod_travel.TravelGroup(user_id=user_id, travel_group_id=tg_id)
                for travel_id in travel_group.get_travel_list():
                    travel = mod_travel.Travel(user_id=user_id, travel_id=travel_id)
                    company_list = travel.get_company_list()
                    if user_id not in company_list:
                        rep_time = travel.get_travel_info().get_date_start()
                        city = travel.get_travel_info().get_city_id()
                        if city not in my_city_list:
                            other_travel_group_list.append({
                                'travel_id': travel_id,
                                'time_delta_days': get_time_delta_days(rep_time),
                                'city_distance': get_city_distance(my_city, city)
                            })

    other_travel_group_list.sort(key=lambda x: ((int(x['city_distance'] / 50)) ** 2 + (int(x["time_delta_days"] / 1)) ** 2))

    return generate_rec_list(other_travel_group_list, amount, key="travel_id")
