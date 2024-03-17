from rest_framework import serializers
from .models import *
from authentications.models import *
from datetime import datetime

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
        fields = ['id','name','location']



class ReportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRecord
        fields = ['component_name','total_number_places_available', 'number_places_rented','occupancy_rate', 'observation']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname','position','email','phone_number']



class ReportSerializer(serializers.ModelSerializer):
    market = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Market.objects.all()
    )
    records = ReportRecordSerializer(many=True)
    created_by = UserSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    forwarded_by = UserSerializer(read_only=True)
    viewed_by = UserSerializer(many=True, read_only=True)
    forwarded_to = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ['id','market', 'season', 'year', 'created_by','created_at', 'verified_by','verified_at', 'approved_by','approved_at', 'forwarded_by', 'viewed_by', 'forwarded_to','forwarded_at', 'status', 'records']
        extra_kwargs = {
            'status': {'default': 'pending'},
            'created_by': {'read_only': True},
            'id':{'read_only':True}
        }

    # def create(self, validated_data):
    #     records_data = validated_data.pop('records')
    #     market = validated_data.get('market')
    #     user = self.context['request'].user

    #     if market.location != user.location:
    #         raise serializers.ValidationError("You can only create a report for a market in your location.")

    #     report = Report.objects.create(**validated_data)
    #     for record_data in records_data:
    #         ReportRecord.objects.create(report=report, **record_data)
    #     return report
        
    
    def create(self, validated_data):
        records_data = validated_data.pop('records')
        market = validated_data.get('market')
        user = self.context['request'].user

        if market.location != user.location:
            raise serializers.ValidationError("You can only create a report for a market in your location.")

        # Determine the year and season based on the current date
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        season = 'Winter' if month in [12, 1, 2] else 'Spring' if month in [3, 4, 5] else 'Summer' if month in [6, 7, 8] else 'Autumn'

        report = Report.objects.create(year=year, season=season, **validated_data)
        for record_data in records_data:
            ReportRecord.objects.create(report=report, **record_data)
        return report
    
    
    
    def get_created_by(self, obj):
        return f"{obj.created_by.firstname} {obj.created_by.lastname}"
    
    
    def update(self, instance, validated_data):
        records_data = validated_data.pop('records')
        instance = super().update(instance, validated_data)

        # Handle the records
        for record_data in records_data:
            record_id = record_data.get('id', None)
            if record_id:
                # Update the record if it already exists
                record = ReportRecord.objects.get(id=record_id, report=instance)
                for attr, value in record_data.items():
                    setattr(record, attr, value)
                record.save()
            else:
                # Create a new record
                ReportRecord.objects.create(report=instance, **record_data)

        return instance
    



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['commented_by', 'report', 'comment', 'created_at']


class CommentListSerializer(serializers.ModelSerializer):
    commented_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['commented_by', 'comment', 'created_at']
