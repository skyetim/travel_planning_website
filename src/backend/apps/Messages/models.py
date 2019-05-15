from django.db import models

import apps.Users.models as Users
import apps.Travels.models as Travels


# Create your models here.
class FriendRequests(models.Model):
    ADD = 'A'
    DELETE = 'D'
    MSG_TYPE_CHOICES = ((ADD, 'Add'),
                        (DELETE, 'Delete'))

    msg_id = models.AutoField(primary_key=True,
                              null=False,
                              editable=False)
    user_id = models.ForeignKey(Users.Users,
                                to_field='user_id',
                                related_name='M_FR_userid',
                                on_delete=models.CASCADE)
    friend_user_id = models.ForeignKey(Users.Users,
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


class TravelAssociation(models.Model):
    INVITE = 'I'
    ADD = 'A'
    LEAVE = 'L'
    MODIFY = 'M'
    DELETE = 'D'
    MSG_TYPE_CHOICES = ((INVITE, 'Invite'),
                        (ADD, 'Add'),
                        (LEAVE, 'Leave'),
                        (MODIFY, 'Modify'),
                        (DELETE, 'Delete'))

    msg_id = models.AutoField(primary_key=True,
                              null=False,
                              editable=False)
    user_id = models.ForeignKey(Users.Users,
                                to_field='user_id',
                                related_name='M_TA_userid',
                                on_delete=models.CASCADE)
    friend_user_id = models.ForeignKey(Users.Users,
                                       to_field='user_id',
                                       related_name='M_TA_frienduserid',
                                       on_delete=models.CASCADE)
    travel_id = models.ForeignKey(Travels.Travels,
                                  to_field='travel_id',
                                  related_name='M_TA_travelid',
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
