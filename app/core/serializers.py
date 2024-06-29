from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import PasswordField




User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = User
        fields = ['password', 'email',"name"]
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, attrs):
        email = attrs['email'].lower()
        name = attrs['name'].title()
        
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        attrs['email'] = email
        attrs['name'] = name
        
        return super().validate(attrs)
        
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
        )
        return user
    
