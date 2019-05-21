from datatime import date as ddate

import apps.db.User.models as db_user
import apps.db.Travel.models as db_travel

import apps.api.modules.city as mod_city
import apps.api.modules.travel as mod_travel
import apps.api.modules.user as mod_user

from apss.api.modules.exceptions import *

def recommend(user_id):
    mod_user.check_user_existance(user_id)

    user_ob = db_user.User.objects.get(user_id=user_id)
    user = mod_user.User(email=user_ob.email, pswd_hash=user_ob.pswd_hash)

    travel_group_list = user.get_group_info_list()

    friend_info_list = user.get_friend_info_list() #FriendInfo Object
    friend_travel_group_list = [] #如何获取朋友的travel信息？
    for friend_info in friend_info_list:
        friend_travel_group_list.append()


    # 对每个travelgroup中的每个travel，按地点，搜索每个friend的每个travelgroup中的每个travel，
    # 若地点相同则匹配日期，若符合，则将，地点，出行日期，好友信息存起
    for travel_group in travel_group_list:
        travel_list = travel_group.get_travel_list()
        for travel in travel_list:
            company_list = travel.get_company_list() # actually user_id_list, database object
            travel_info = travel.get_travel_info() # TravelInfo Object



