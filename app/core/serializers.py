from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

User = auth.get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'name',
                  'is_active', 'is_staff', 'password']
        read_only_fields = ['is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

        def validate(self, attrs):
            email = attrs.get('email', '')
            password = attrs.get('password', '')
            user = auth.authenticate(email=email, password=password)
            if not user:
                raise AuthenticationFailed('Invalid credentials, try again')
            attrs['user'] = user
            return attrs
