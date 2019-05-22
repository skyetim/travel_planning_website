from rest_framework import serializers

from apps.db.City.serializers import CitySerializer
from apps.db.Travel.models import TravelGroupOwnership, TravelGroup, TravelGrouping, Travel, TravelAssociation


class TravelAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelAssociation
        fields = ['travel_id', 'company_user_id']


class TravelSerializer(serializers.ModelSerializer):
    city = CitySerializer(source='city_id', many=False, read_only=True)
    travel_association = TravelAssociationSerializer(source='T_TA_travelid', many=True, read_only=True)

    class Meta:
        model = Travel
        fields = ['travel_id',
                  'date_start', 'date_end',
                  'city',
                  'visibility',
                  'travel_note',
                  'travel_association']


class TravelGroupingSerializer(serializers.ModelSerializer):
    travel = TravelSerializer(source='travel_id', many=False, read_only=True)

    class Meta:
        model = TravelGrouping
        fields = ['travel']


class TravelGroupSerializer(serializers.ModelSerializer):
    travel_grouping = TravelGroupingSerializer('T_TG_travelgroupid', many=True, read_only=True)

    class Meta:
        model = TravelGroup
        fields = ['travel_group_id',
                  'travel_group_name',
                  'travel_group_note',
                  'travel_group_color',
                  'travel_grouping']


class GroupOwnershipSerializer(serializers.ModelSerializer):
    travel_group = TravelGroupSerializer(source='travel_group_id', many=True, read_only=True)

    class Meta:
        model = TravelGroupOwnership
        fields = ['user_id', 'travel_group']
