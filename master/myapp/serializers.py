from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    role_id = serializers.IntegerField(write_only=True, required=False)
    is_active = serializers.IntegerField(required=False)
    created_by = serializers.CharField(required=False)
    updated_by = serializers.CharField(required=False)

    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password', 'phone', 'role_id', 'is_active', 'updated_by','created_by']

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        role_id = validated_data.pop('role_id', None)
        created_by = validated_data.pop('created_by', "SYSTEM")
        user = AuthUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data.get('password')
        )

        role_instance = None
        if role_id:
            try:
                role_instance = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                pass

        Profile.objects.create(
            user=user,
            name=user.username,
            phone=phone,
            email=user.email,
            role=role_instance,
            is_active=2,
            password=validated_data.get('password'),
            created_by= created_by,
        )

        return user

    def update(self, instance, validated_data):
        phone = validated_data.pop('phone', None)
        role_id = validated_data.pop('role_id', None)
        is_active = validated_data.pop('is_active', None)
        password = validated_data.pop('password', None)
        updated_by = validated_data.pop('updated_by', None)

        # Update User table
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        if password and password.strip():
            instance.set_password(password)
        instance.save()

        # Update Profile table
        try:
            print(is_active)
            profile = Profile.objects.get(user=instance)

            profile.name = instance.username
            profile.email = instance.email

            if password and password.strip():
                profile.password = password

            if is_active is not None:
                profile.is_active = is_active

            if phone is not None:
                profile.phone = phone
            if updated_by is not None:
                profile.updated_by = updated_by
                profile.updated_at = timezone.now()

            if role_id:
                try:
                    profile.role = Role.objects.get(id=role_id)
                except Role.DoesNotExist:
                    pass

            profile.save()

        except Profile.DoesNotExist:
            pass

        return instance

class ProfileSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name')
    class Meta:
        model = Profile
        fields = '__all__'