from django.db import models

import apps.Cities.models as Cities
import apps.Users.models as Users


# Create your models here.
class TravelGroups(models.Model):
    travel_group_id = models.AutoField(primary_key=True,
                                       null=False,
                                       unique=True,
                                       editable=False)
    travel_group_note = models.TextField(max_length=140,
                                         null=False,
                                         editable=True)

    class Meta:
        indexes = [
            models.Index(fields=['travel_group_id'],
                         name='TG_idx')
        ]


class TravelGroupOwnership(models.Model):
    user_id = models.ForeignKey(Users.Users,
                                to_field='user_id',
                                on_delete=models.CASCADE)
    travel_group_id = models.OneToOneField(TravelGroups,
                                           to_field='travel_group_id',
                                           unique=True,
                                           on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['user_id'],
                         name='TGO_userid_idx'),
            models.Index(fields=['travel_group_id'],
                         name='TGO_travelgroupid_idx')
        ]


class Travels(models.Model):
    ONLY_ME = 'M'
    FRIEND = 'F'
    PUBLIC = 'P'
    VISIBILITY_CHOICES = ((ONLY_ME, 'Only Me'),
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
    city_id = models.ForeignKey(Cities.Cities,
                                to_field='city_id',
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
                         name='T_travelid_idx'),
            models.Index(fields=['date_start'],
                         name='T_datestart_idx'),
            models.Index(fields=['date_end'],
                         name='T_dateend_idx'),
            models.Index(fields=['city_id'],
                         name='T_cityid_idx'),
            models.Index(fields=['visibility'],
                         name='T_visibility_idx')
        ]


class TravelGrouping(models.Model):
    travel_id = models.OneToOneField(Travels,
                                     to_field='travel_id',
                                     unique=True,
                                     on_delete=models.CASCADE)
    travel_group_id = models.OneToOneField(TravelGroups,
                                           to_field='travel_group_id',
                                           unique=True,
                                           on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['travel_id'],
                         name='TG_travelid_idx'),
            models.Index(fields=['travel_group_id'],
                         name='TG_travelgroupid_idx')
        ]


class TravelAssociation(models.Model):
    travel_id = models.ForeignKey(Travels,
                                  to_field='travel_id',
                                  on_delete=models.CASCADE)
    company_user_id = models.ForeignKey(Users.Users,
                                        to_field='user_id',
                                        related_name='company_user_id',
                                        on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['travel_id'],
                         name='TA_travelid_idx'),
            models.Index(fields=['company_user_id'],
                         name='TA_companyuserid_idx')
        ]
        unique_together = (('travel_id', 'company_user_id'),)
