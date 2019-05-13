from django.db import models


# Create your models here.
class Cities(models.Model):
    city_id = models.AutoField(primary_key=True,
                               db_index=True,
                               null=False,
                               unique=True,
                               editable=False)
    country_name = models.CharField(max_length=20,
                                    db_index=True,
                                    null=False,
                                    editable=False)
    province_name = models.CharField(max_length=20,
                                     db_index=True,
                                     null=False,
                                     editable=False)
    city_name = models.CharField(max_length=20,
                                 db_index=True,
                                 editable=False)
    latitude = models.FloatField(null=False,
                                 editable=False)
    longitude = models.FloatField(null=False,
                                  editable=False)

    class Meta:
        unique_together = (('country_name', 'province_name', 'city_name'),)
