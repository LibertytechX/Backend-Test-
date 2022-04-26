from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=32, write_only=True)
    email = serializers.EmailField(max_length=50, allow_blank=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}
                        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
