from rest_framework import serializers
from .models import *

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


class MarketSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Location.objects.all()
    )

    class Meta:
        model = Market
        fields = ['name','location']



class ReportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRecord
        fields = ['component_name', 'component_description', 'total_number_places_available', 'number_places_rented','occupancy_rate', 'observation']

class ReportSerializer(serializers.ModelSerializer):
    market = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Market.objects.all()
    )
    records = ReportRecordSerializer(many=True)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['market', 'season', 'year', 'created_by', 'verified_by', 'approved_by', 'forwarded_by', 'viewed_by', 'forwarded_to', 'status', 'records']
        extra_kwargs = {
            'status': {'default': 'pending'},
            'created_by': {'read_only': True}
        }

    def create(self, validated_data):
        records_data = validated_data.pop('records')
        market = validated_data.get('market')
        user = self.context['request'].user

        if market.location != user.location:
            raise serializers.ValidationError("You can only create a report for a market in your location.")

        report = Report.objects.create(**validated_data)
        for record_data in records_data:
            ReportRecord.objects.create(report=report, **record_data)
        return report
    
    def get_created_by(self, obj):
        return f"{obj.created_by.firstname} {obj.created_by.lastname}"