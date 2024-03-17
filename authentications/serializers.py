# serializers.py
from rest_framework import serializers
import re
from .models import User
from marketrecord.models import Location

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(min_length=13, max_length=13)
    role = serializers.StringRelatedField() 
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ['id','email', 'firstname', 'lastname', 'phone_number', 'role', 'password', 'position', 'location', 'is_approved', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        """
        Validate whether the password meets all requirements.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    def to_internal_value(self, data):
        location_name = data.get('location')
        if location_name:
            location = Location.objects.filter(name=location_name).first()
            if location:
                data['location'] = location
            else:
                raise serializers.ValidationError({"location": "Location with this name does not exist."})
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        if email == '':
            raise serializers.ValidationError('Email is required')
        if password == '':
            raise serializers.ValidationError('Password is required')

        return data

  

class UserUpdateSerializer(serializers.Serializer):
    is_approved = serializers.BooleanField(required=False)
    role = serializers.CharField(max_length=10, required=False)

