from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()

class UserRegistrationSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email','name', 'password', 'confirm_password']

        extra_kwargs = {
            "password":{"write_only":True},
            "confirm_password":{"write_only":True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
       
        try:
            password_validation.validate_password(attrs['password'])
        except ValidationError as err:
            raise serializers.ValidationError(
            {"password": err.messages})
        return attrs
    
    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)

        user.set_password(password)
        user.save()

        return user





class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

    
