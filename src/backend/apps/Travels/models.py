from django.db import models

import apps.Cities.models as Cities
import apps.Users.models as Users


# Create your models here.
class TravelGroups(models.Model):
    travel_groups_id = models.AutoField(primary_key=True,
                                        db_index=True,
                                        null=False,
                                        unique=True,
                                        editable=False)
    travel_groups_note = models.TextField(max_length=140,
                                          null=False,
                                          editable=True)


class TravelGroupOwnership(models.Model):
    user_id = models.ForeignKey(Users.Users,
                                to_field='user_id',
                                db_index=True,
                                on_delete=models.CASCADE)
    travel_groups_id = models.OneToOneField(TravelGroups,
                                            to_field='travel_groups_id',
                                            db_index=True,
                                            unique=True,
                                            on_delete=models.CASCADE)


class Travels(models.Model):
    ONLY_ME = 'M'
    FRIEND = 'F'
    PUBLIC = 'P'
    VISIBILITY_CHOICES = ((ONLY_ME, 'Only Me'),
                          (FRIEND, 'Friend'),
                          (PUBLIC, 'Public'))

    travel_id = models.AutoField(primary_key=True,
                                 db_index=True,
                                 null=False,
                                 unique=True,
                                 editable=False)
    data_start = models.DateField(db_index=True,
                                  null=False,
                                  editable=True)
    data_end = models.DateField(db_index=True,
                                null=False,
                                editable=True)
    city_id = models.ForeignKey(Cities.Cities,
                                to_field='city_id',
                                db_index=True,
                                on_delete=models.PROTECT)
    visibility = models.CharField(max_length=1,
                                  default=FRIEND,
                                  choices=VISIBILITY_CHOICES,
                                  null=False,
                                  editable=True)
    travel_note = models.TextField(max_length=140,
                                   null=False,
                                   editable=True)


class TravelGrouping(models.Model):
    travel_id = models.OneToOneField(Travels,
                                     to_field='travel_id',
                                     db_index=True,
                                     unique=True,
                                     on_delete=models.CASCADE)
    travel_groups_id = models.OneToOneField(TravelGroups,
                                            to_field='travel_groups_id',
                                            db_index=True,
                                            unique=True,
                                            on_delete=models.CASCADE)


class TravelAssociation(models.Model):
    travel_id = models.ForeignKey(Travels,
                                  to_field='travel_id',
                                  db_index=True,
                                  on_delete=models.CASCADE)
    company_user_id = models.ForeignKey(Users.Users,
                                        to_field='user_id',
                                        related_name='company_user_id',
                                        db_index=True,
                                        on_delete=models.CASCADE)

    class Meta:
        unique_together = (('travel_id', 'company_user_id'),)
