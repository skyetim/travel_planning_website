from rest_framework import serializers

from apps.db.Travel.models import TravelGroup, TravelGrouping, Travel, TravelAssociation


class TravelAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelAssociation
        fields = [field.name for field in TravelAssociation._meta.get_fields()]


class TravelSerializer(serializers.ModelSerializer):
    travel_association = TravelAssociationSerializer(many=True, read_only=True)

    class Meta:
        model = Travel
        fields = [field.name for field in Travel._meta.get_fields()]
        fields.append('travel_association')


class TravelGroupingSerializer(serializers.ModelSerializer):
    travels = TravelSerializer(many=False, read_only=True)

    class Meta:
        model = TravelGrouping
        fields = [field.name for field in TravelGrouping._meta.get_fields()]
        fields.append('travels')


class TravelGroupSerializer(serializers.ModelSerializer):
    travel_grouping = TravelGroupingSerializer(many=False, read_only=True)

    class Meta:
        model = TravelGroup
        fields = [field.name for field in TravelGroup._meta.get_fields()]
        fields.append('travel_grouping')
