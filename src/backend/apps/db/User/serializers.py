from rest_framework import serializers

from apps.db.Travel.serializers import TravelGroupSerializer
from apps.db.User.models import User, UserInfo, FriendRelation


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = UserInfo._meta.get_fields()


class FriendRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRelation
        fields = FriendRelation._meta.get_fields()


class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(many=False, read_only=True)
    friend_relation = FriendRelationSerializer(many=True, read_only=True)
    travel_groups = TravelGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = User._meta.get_fields()
        fields.append('user_info')
        fields.append('friend_relation')
        fields.append('travel_groups')
