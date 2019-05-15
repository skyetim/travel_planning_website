import uuid

from django.db import models

import apps.db.City.models as city


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True,
                               null=False,
                               editable=False)
    email = models.EmailField(null=False,
                              unique=True,
                              editable=True)
    pswd_hash = models.CharField(max_length=32,
                                 null=False,
                                 editable=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='U_U_userid_idx'),
            models.Index(fields=['email'],
                         name='U_U_email_idx')
        ]


class UserInfo(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    OTHER = 'O'
    GENDER_CHOICES = ((MALE, 'Male'),
                      (FEMALE, 'Female'),
                      (UNKNOWN, 'Unknown'),
                      (OTHER, 'Other'))

    user_id = models.OneToOneField(User,
                                   to_field='user_id',
                                   related_name='U_UI_userid',
                                   primary_key=True,
                                   unique=True,
                                   on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20,
                                 null=False,
                                 editable=True)
    gender = models.CharField(max_length=1,
                              default=UNKNOWN,
                              choices=GENDER_CHOICES,
                              null=False,
                              editable=True)
    resident_city_id = models.ForeignKey(city.City,
                                         to_field='city_id',
                                         related_name='U_UI_residentcityid',
                                         on_delete=models.PROTECT)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='U_UI_userid_idx'),
        ]


class FriendRelation(models.Model):
    user_id = models.ForeignKey(User,
                                to_field='user_id',
                                related_name='U_FR_userid',
                                on_delete=models.CASCADE)
    friend_user_id = models.ForeignKey(User,
                                       to_field='user_id',
                                       related_name='U_FR_frienduserid',
                                       on_delete=models.CASCADE)
    friend_user_note = models.CharField(max_length=20,
                                        null=False,
                                        editable=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='U_FR_userid_idx'),
            models.Index(fields=['user_id', 'friend_user_id'],
                         name='U_FR_idx'),
        ]
        unique_together = (('user_id', 'friend_user_id'),)


class UserSession(models.Model):
    user_id = models.OneToOneField(User,
                                   to_field='user_id',
                                   related_name='U_US_userid',
                                   primary_key=True,
                                   unique=True,
                                   on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4,
                                  editable=False,
                                  unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='U_US_userid_idx')
        ]
