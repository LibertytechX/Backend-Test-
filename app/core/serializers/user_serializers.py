from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers, exceptions as jwt_exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import User


class CustomerSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.role = "CUSTOMER"
        user.save()
        return user


class StaffSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.role = "STAFF"
        user.is_staff = True
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'role', 'email', 'name')


# class UserSerializerToken(UserSerializer):
#     # token = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'name', 'email', 'role', 'emailVerifield')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     token["username"] = user.username
    #     token["greet"] = "hello word"

    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data
