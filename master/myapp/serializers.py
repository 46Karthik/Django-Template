from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User as AuthUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password','phone']

    def create(self, validated_data):
        # Extract profile-specific fields (phone, address)
        phone = validated_data.pop('phone')

        # Create the AuthUser instance
        user = AuthUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create the Profile instance with username as name
        Profile.objects.create(
            user=user,
            name=user.username,  # Set the profile name as the username
            phone=phone,
            email=validated_data['email'],  # Profile email can be the same as user email
            is_active=False  # Initially inactive
        )

        return user
