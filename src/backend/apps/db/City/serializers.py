from rest_framework import serializers

from apps.db.City.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'city_id',
            'country_name', 'province_name', 'city_name',
            'latitude', 'longitude'
        ]
