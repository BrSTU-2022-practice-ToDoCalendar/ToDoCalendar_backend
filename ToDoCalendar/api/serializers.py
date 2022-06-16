from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import User, Task


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value):
            raise ValidationError('A user with that email already exists.')
        return value

    def validate_password(self, value):
        return make_password(value)


# class TaskSerializer(serializers.ModelSerializer):
