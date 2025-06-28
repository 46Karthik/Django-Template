from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User as AuthUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    role_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password', 'phone', 'role_id']

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        role_id = validated_data.pop('role_id', None)

        user = AuthUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        role_instance = None
        if role_id:
            try:
                role_instance = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                pass  # Optional: raise ValidationError if role is invalid

        Profile.objects.create(
            user=user,
            name=user.username,
            phone=phone,
            email=validated_data['email'],
            role=role_instance,
            is_active=False
        )

        return user
