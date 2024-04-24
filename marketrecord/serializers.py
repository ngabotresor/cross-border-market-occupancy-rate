from rest_framework import serializers
from .models import *
from authentications.models import *
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'name', 'market', 'total_number_places_available']
        
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
        fields = ['id','component_name','total_number_places_available', 'number_places_rented','occupancy_rate', 'observation']

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
        # season = 'Winter' if month in [12, 1, 2] else 'Spring' if month in [3, 4, 5] else 'Summer' if month in [6, 7, 8] else 'Autumn'

        report = Report.objects.create(**validated_data)
        for record_data in records_data:
            
            if record_data['total_number_places_available'] < record_data['number_places_rented']:
                raise serializers.ValidationError("The number of places rented cannot be greater than the total number of places available.")
            
            ReportRecord.objects.create(report=report, **record_data)
        # Send email after report is created
        subject = 'A new report has been created'
        message = f'Report with id:{report.id} has been created by {user.firstname} {user.lastname} at {report.created_at}.'
        email_from = settings.EMAIL_HOST_USER  
        users_same_location = User.objects.filter(
            location=report.created_by.location,
             role__in=[1,3,4,5]
            )
        recipient_list = [user.email for user in users_same_location]
        send_mail(subject, message, email_from,recipient_list)
        return report
    
    
    
    def get_created_by(self, obj):
        return f"{obj.created_by.firstname} {obj.created_by.lastname}"
    
    
    def update(self, instance, validated_data):
        records_data = validated_data.pop('records', []) 
        existing_records = {record.id: record for record in instance.records.all()}
        updated_records = []
        for record_data in records_data:
            record_id = record_data.get('id')
            if record_id:
                # Update existing ReportRecord instance
                record_instance = existing_records.pop(record_id, None)
                if record_instance:
                    record_serializer = ReportRecordSerializer(instance=record_instance, data=record_data)
                else:
                    continue  # Skip if record with provided ID doesn't exist
            else:
                # Create new ReportRecord instance
                record_serializer = ReportRecordSerializer(data=record_data)

            if record_serializer.is_valid():
                updated_record = record_serializer.save(report=instance)  # Assign report to the record
                updated_records.append(updated_record)

        # Delete remaining ReportRecord instances that were not updated
        for record in existing_records.values():
            record.delete()

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
