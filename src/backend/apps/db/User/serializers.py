from rest_framework import serializers

from apps.db.City.serializers import CitySerializer
from apps.db.Travel.serializers import GroupOwnershipSerializer
from apps.db.User.models import User, UserInfo, FriendRelation


class UserInfoSerializer(serializers.ModelSerializer):
    resident_city = CitySerializer(source='resident_city_id', many=False, read_only=True)

    class Meta:
        model = UserInfo
        fields = ['user_id',
                  'user_name',
                  'gender',
                  'resident_city']


class FriendRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRelation
        fields = ['friend_user_id',
                  'friend_note']


class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(source='U_UI_userid', many=False, read_only=True)
    friend_list = FriendRelationSerializer(source='U_FR_userid', many=True, read_only=True)
    travel_group_list = GroupOwnershipSerializer(source='T_TGO_userid', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id',
                  'email',
                  'user_info',
                  'friend_list',
                  'travel_group_list']
