from datetime import date as ddate

import apps.db.User.models as db_user
import apps.db.Travel.models as db_travel

import apps.api.modules.city as mod_city
import apps.api.modules.travel as mod_travel
import apps.api.modules.user as mod_user

from apps.api.modules.exceptions import *


# def recommend(user_id):
#     mod_user.check_user_existence(user_id)

#     user_ob = db_user.User.objects.get(user_id=user_id)
#     user = mod_user.User(email=user_ob.email, pswd_hash=user_ob.pswd_hash)

#     travel_group_list = user.get_group_info_list()

#     friend_info_list = user.get_friend_list()  # FriendInfo Object
#     friend_travel_group_list = []  # 如何获取朋友的travel信息？
#     for friend_info in friend_info_list:
#         friend_travel_group_list.append()

#     # 对每个travelgroup中的每个travel，按地点，搜索每个friend的每个travelgroup中的每个travel，
#     # 若地点相同则匹配日期，若符合，则将，地点，出行日期，好友信息存起
#     for travel_group in travel_group_list:
#         travel_list = travel_group.get_travel_list()
#         for travel in travel_list:
#             # actually user_id_list, database object
#             company_list = travel.get_company_list()
#             travel_info = travel.get_travel_info()  # TravelInfo Object


# 以下所有user如无意外均指User类的实例对象

def recommend_friend_list(user, amount=10):
    # 从用户数据库中找不是自己好友的那些
    # 根据所在城市、去过的城市等进行匹配推荐（随机抽取）
    # 不要求高精度排序
    # 总数不超过amount
    user_id_list = []
    return user_id_list


def recommend_travel_group_list(user, amount=10):
    # 遍历好友的旅行记录
    # 根据时间和今天的距离排序进行推荐
    # 总数不超过amount
    friend_list=user.get_friend_list()
    other_travel_group_list=[]

    return


def recommend_city_list_by_travel(user_id, travel_id, amount=3):
    # 遍历好友的旅行记录
    # 根据城市和该travel的距离排序进行推荐
    # 不包括本城市
    # 总数不超过amount
    return


def recommend_city_list_by_travel_group(user_id, travel_group_id, amount=3):
    # 遍历好友的旅行记录
    # 根据城市和该travel_group中已有的距离排序进行推荐
    # 不包括该travel_group中已有的city
    # 总数不超过amount
    return


def recommend_travel_list_by_travel(user_id, travel_id, amount=5):
    # 遍历好友的旅行记录
    # 根据城市和该travel的距离、时间间隔排序进行推荐
    # 总数不超过amount
    return


def recommend_travel_list_by_travel_group(user_id, travel_group_id, amount=5):
    # 遍历好友的旅行记录
    # 根据城市和该travel_group中城市的距离、时间间隔排序进行推荐
    # 总数不超过amount
    return
