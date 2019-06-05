from django.db import models

import apps.db.Travel.models as travel
import apps.db.User.models as user


# Create your models here.
class FriendRequest(models.Model):
    ADD = 'A'
    DELETE = 'D'
    MSG_TYPE_CHOICES = ((ADD, 'Add'),
                        (DELETE, 'Delete'))

    msg_id = models.AutoField(primary_key=True,
                              null=False,
                              editable=False)
    user_id = models.ForeignKey(user.User,
                                to_field='user_id',
                                related_name='M_FR_userid',
                                on_delete=models.CASCADE)
    friend_user_id = models.ForeignKey(user.User,
                                       to_field='user_id',
                                       related_name='M_FR_frienduserid',
                                       on_delete=models.CASCADE)
    msg_type = models.CharField(max_length=1,
                                default=ADD,
                                choices=MSG_TYPE_CHOICES,
                                null=False,
                                editable=False)
    msg_content = models.TextField(max_length=140,
                                   null=False,
                                   editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['msg_id'],
                         name='M_FR_msgid_idx'),
            models.Index(fields=['user_id'],
                         name='M_FR_userid_idx')
        ]

    def keys(self):
        return ['msg_id',
                'user_id',
                'friend_user_id',
                'msg_type',
                'msg_content']

    def __getitem__(self, item):
        if 'user_id' in item:
            return getattr(self, item).user_id
        else:
            return getattr(self, item)


class TravelAssociation(models.Model):
    INVITE = 'I'
    ADD = 'A'
    REMOVE = 'R'
    LEAVE = 'L'
    MODIFY = 'M'
    DELETE = 'D'
    MSG_TYPE_CHOICES = ((INVITE, 'Invite'),
                        (ADD, 'Add'),
                        (REMOVE, 'Remove'),
                        (LEAVE, 'Leave'),
                        (MODIFY, 'Modify'),
                        (DELETE, 'Delete'))

    msg_id = models.AutoField(primary_key=True,
                              null=False,
                              editable=False)
    user_id = models.ForeignKey(user.User,
                                to_field='user_id',
                                related_name='M_TA_userid',
                                on_delete=models.CASCADE)
    friend_user_id = models.ForeignKey(user.User,
                                       to_field='user_id',
                                       related_name='M_TA_frienduserid',
                                       on_delete=models.CASCADE)
    travel_id = models.ForeignKey(travel.Travel,
                                  to_field='travel_id',
                                  related_name='M_TA_travelid',
                                  null=True,
                                  on_delete=models.CASCADE)
    msg_type = models.CharField(max_length=1,
                                choices=MSG_TYPE_CHOICES,
                                null=False,
                                editable=False)
    msg_content = models.TextField(max_length=140,
                                   null=False,
                                   editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['msg_id'],
                         name='M_TA_msgid_idx'),
            models.Index(fields=['user_id'],
                         name='M_TA_userid_idx')
        ]

    def keys(self):
        return ['msg_id',
                'user_id',
                'friend_user_id',
                'travel_id',
                'msg_type',
                'msg_content']

    def __getitem__(self, item):
        if 'user_id' in item:
            return getattr(self, item).user_id
        elif 'travel_id' in item:
            return getattr(self, item).travel_id
        else:
            return getattr(self, item)
