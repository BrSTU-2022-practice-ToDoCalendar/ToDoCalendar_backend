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
        fields = (
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'completed',
            'user',
        )
        read_only_fields = ('id', 'user')
        extra_kwargs = {
            'title': {
                'required': True, 'allow_blank': False, 'allow_null': True
                },
            'description': {'allow_null': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
        }

    def validate(self, value):
        super().validate(value)
        start = (value['start_date'] if 'start_date' in value
                 else self.instance.start_date)

        end = (value['end_date'] if 'end_date' in value
               else self.instance.end_date)

        if start >= end:
            raise serializers.ValidationError(
                {'date': 'End date must be greater than start date.'}
            )

        return value
