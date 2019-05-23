from django.db import models

import apps.db.City.models as city
import apps.db.User.models as users


# Create your models here.
class TravelGroup(models.Model):
    travel_group_id = models.AutoField(primary_key=True,
                                       null=False,
                                       unique=True,
                                       editable=False)
    travel_group_name = models.CharField(max_length=20,
                                         default='未命名',
                                         null=False,
                                         editable=True)
    travel_group_note = models.TextField(max_length=140,
                                         null=False,
                                         editable=True)
    travel_group_color = models.PositiveIntegerField(null=False,
                                                     editable=True)

    class Meta:
        indexes = [
            models.Index(fields=['travel_group_id'],
                         name='T_TG_idx')
        ]


class TravelGroupOwnership(models.Model):
    user_id = models.ForeignKey(users.User,
                                to_field='user_id',
                                related_name='T_TGO_userid',
                                on_delete=models.CASCADE)
    travel_group_id = models.OneToOneField(TravelGroup,
                                           to_field='travel_group_id',
                                           related_name='T_TGO_travelgroupid',
                                           unique=True,
                                           on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='T_TGO_userid_idx'),
            models.Index(fields=['travel_group_id'],
                         name='T_TGO_travelgroupid_idx')
        ]


class Travel(models.Model):
    ME = 'M'
    FRIEND = 'F'
    PUBLIC = 'P'
    VISIBILITY_CHOICES = ((ME, 'Only Me'),
                          (FRIEND, 'Friend'),
                          (PUBLIC, 'Public'))

    travel_id = models.AutoField(primary_key=True,
                                 null=False,
                                 unique=True,
                                 editable=False)
    date_start = models.DateField(null=False,
                                  editable=True)
    date_end = models.DateField(null=False,
                                editable=True)
    city_id = models.ForeignKey(city.City,
                                to_field='city_id',
                                related_name='T_T_cityid',
                                on_delete=models.PROTECT)
    visibility = models.CharField(max_length=1,
                                  default=FRIEND,
                                  choices=VISIBILITY_CHOICES,
                                  null=False,
                                  editable=True)
    travel_note = models.TextField(max_length=140,
                                   null=False,
                                   editable=True)

    class Meta:
        indexes = [
            models.Index(fields=['travel_id'],
                         name='T_T_travelid_idx'),
            models.Index(fields=['date_start'],
                         name='T_T_datestart_idx'),
            models.Index(fields=['date_end'],
                         name='T_T_dateend_idx'),
            models.Index(fields=['city_id'],
                         name='T_T_cityid_idx'),
            models.Index(fields=['visibility'],
                         name='T_T_visibility_idx')
        ]


class TravelGrouping(models.Model):
    travel_id = models.OneToOneField(Travel,
                                     to_field='travel_id',
                                     related_name='T_TG_travelid',
                                     unique=False,
                                     on_delete=models.CASCADE)
    travel_group_id = models.OneToOneField(TravelGroup,
                                           to_field='travel_group_id',
                                           related_name='T_TG_travelgroupid',
                                           unique=True,
                                           on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['travel_id'],
                         name='T_TG_travelid_idx'),
            models.Index(fields=['travel_group_id'],
                         name='T_TG_travelgroupid_idx')
        ]


class TravelAssociation(models.Model):
    travel_id = models.ForeignKey(Travel,
                                  to_field='travel_id',
                                  related_name='T_TA_travelid',
                                  on_delete=models.CASCADE)
    company_user_id = models.ForeignKey(users.User,
                                        to_field='user_id',
                                        related_name='T_TA_companyuserid',
                                        on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['travel_id'],
                         name='T_TA_travelid_idx'),
            models.Index(fields=['company_user_id'],
                         name='T_TA_companyuserid_idx')
        ]
        unique_together = (('travel_id', 'company_user_id'),)
