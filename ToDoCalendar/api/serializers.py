from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


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