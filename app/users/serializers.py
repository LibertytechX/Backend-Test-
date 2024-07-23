from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id', 'email', 'name', 'password1', 'password2']

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        check_email = User.objects.filter(email=email)
        if check_email.exists():
            raise serializers.ValidationError("email is already in use!")
        if password1 != password2:
            raise serializers.ValidationError("passwords do not match!")
        return attrs
    
    def create(self, validated_data):
        user= User.objects.create_user(
            email=validated_data['email'],
            name=validated_data.get('name'), 
            password=validated_data.get('password1')
            )
        return user
