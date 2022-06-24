from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Task


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}
        }

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value):
            raise serializers.ValidationError(
                'A user with this email already exist'
            )
        return value

    def validate_password(self, value):
        return make_password(value)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'user')
        read_only_fields = ('id')
        extra_kwargs = {
            'title': {
                'required': True, 'allow_blank': False, 'allow_null': True
                },
            'description':{'allow_null': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'user': {'write_only': True},
        }

    def validate(self, value):
        super().validate(value)
        if value.start_date>value.end_date:
            raise serializers.ValidationError(
                'Start date is greater than end date'
            )
        return value