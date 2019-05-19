from rest_framework import serializers

from apps.db.City.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = City._meta.get_fields()
