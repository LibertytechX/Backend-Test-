from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from app.modules.utils import api_response
from app.modules.exceptions import InvalidRequestException
from customer.models import CustomerDetail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = super().create(validated_data)
        print(user)
        return CreateUserSerializerOut(
            user, context={"request": self.context.get("request")}
        ).data
        
        
class CreateUserSerializerOut(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class LoginSerializerIn(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        
        
        user = User.objects.filter(username=username).first()
        if user:
            if user.is_authenticated:
                return user
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            response = api_response(message="Invalid email or password", status=False)
            raise InvalidRequestException(response)
        


        user_profile = CustomerDetail.objects.get_or_create(user=user)

        return user


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']



class CustomerSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = CustomerDetail
        fields = ['username', 'first_name', 'email','last_name', 'address', 'phone', 'state', 'country']
        
    def update(self, instance : CustomerDetail, validated_data):
        user : User = instance.user
        
        user_details : dict = validated_data.pop('user', None)
        if user_details:
            first_name = user_details.get('first_name', None)
            last_name = user_details.get('last_name', None)
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance