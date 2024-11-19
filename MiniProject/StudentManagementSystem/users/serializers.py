from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

CustomUser = get_user_model()


class CustomUserCreateSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)

    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default='Student')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 're_password', 'role']

    def validate(self, data):
        if data['password'] != data['re_password']:
            raise ValidationError({"re_password": "Пароли не совпадают!"})
        return data

    def create(self, validated_data):
        validated_data.pop('re_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
        )
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
