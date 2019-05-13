from django.db import models

import apps.Cities.models as Cities


# Create your models here.
class Users(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    OTHER = 'O'
    GENDER_CHOICES = ((MALE, 'Male'),
                      (FEMALE, 'Female'),
                      (UNKNOWN, 'Unknown'),
                      (OTHER, 'Other'))

    user_id = models.AutoField(primary_key=True,
                               null=False,
                               editable=False)
    email = models.EmailField(null=False,
                              unique=True,
                              editable=True)
    user_name = models.CharField(max_length=20,
                                 null=False,
                                 editable=True)
    pswd_hash = models.BinaryField(max_length=16,
                                   null=False,
                                   editable=True)
    gender = models.CharField(max_length=1,
                              default=UNKNOWN,
                              choices=GENDER_CHOICES,
                              null=False,
                              editable=True)
    resident_city_id = models.ForeignKey(Cities.Cities,
                                         to_field='city_id',
                                         related_name='resident_city_id',
                                         on_delete=models.PROTECT)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='U_userid_idx'),
            models.Index(fields=['email'],
                         name='U_email_idx')
        ]


class FriendRelations(models.Model):
    user_id = models.ForeignKey(Users,
                                to_field='user_id',
                                related_name='my_user_id',
                                on_delete=models.CASCADE)
    friend_user_id = models.ForeignKey(Users,
                                       to_field='user_id',
                                       related_name='friend_user_id',
                                       on_delete=models.CASCADE)
    friend_user_note = models.CharField(max_length=20,
                                        null=False,
                                        editable=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='FR_userid_idx'),
            models.Index(fields=['user_id', 'friend_user_id'],
                         name='FR_idx'),
        ]
        unique_together = (('user_id', 'friend_user_id'),)
