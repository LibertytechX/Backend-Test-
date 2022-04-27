from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            user.save()
            return user