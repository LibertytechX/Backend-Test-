from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("email", "password", "name", "is_staff")

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
