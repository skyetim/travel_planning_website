from django.db import models


# Create your models here.
class City(models.Model):
    city_id = models.AutoField(primary_key=True,
                               null=False,
                               unique=True,
                               editable=False)
    country_name = models.CharField(max_length=20,
                                    null=False,
                                    editable=False)
    province_name = models.CharField(max_length=20,
                                     null=False,
                                     editable=False)
    city_name = models.CharField(max_length=20,
                                 editable=False)
    latitude = models.FloatField(null=False,
                                 editable=False)
    longitude = models.FloatField(null=False,
                                  editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['city_id'],
                         name='C_cityid_idx'),
            models.Index(fields=['country_name', 'province_name', 'city_name'],
                         name='C_cityname_idx')
        ]
        unique_together = (('country_name', 'province_name', 'city_name'),)

    def keys(self):
        return ['city_id',
                'country_name',
                'province_name',
                'city_name',
                'latitude',
                'longitude']

    def __getitem__(self, item):
        return getattr(self, item)
