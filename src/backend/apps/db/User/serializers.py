from rest_framework import serializers

from apps.db.Travel.serializers import TravelGroupSerializer
from apps.db.User.models import User, UserInfo, FriendRelation


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user_id',
                  'user_name',
                  'gender',
                  'resident_city_id']


class FriendRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRelation
        fields = ['user_id',
                  'friend_user_id',
                  'friend_user_note']


class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(many=False, read_only=True)
    friend_relation = FriendRelationSerializer(many=True, read_only=True)
    travel_groups = TravelGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id',
                  'email',
                  'user_info',
                  'friend_relation',
                  'travel_groups']
