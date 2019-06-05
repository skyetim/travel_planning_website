from rest_framework import serializers

from apps.db.Message.models import FriendRequest
from apps.db.User.serializers import UserInfoSerializer


class FriendRequestSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(source='user_id.U_UI_userid', many=False, read_only=True)
    friend_user_info = UserInfoSerializer(source='friend_user_id.U_UI_userid', many=False, read_only=True)

    class Meta:
        model = FriendRequest
        fields = [
            'msg_id',
            'user_info', 'friend_user_info',
            'msg_type', 'msg_content'
        ]
