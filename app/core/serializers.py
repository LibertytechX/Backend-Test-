from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Product, Category, Order, OrderProduct

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['name'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    data['access'] = str(refresh.access_token)
                    data['refresh'] = str(refresh)
                else:
                    raise serializers.ValidationError("User is not active.")
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include both username and password.")

        return data






class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category']

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproduct_set', many=True)  # Use the reverse relation name

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'date']

    def create(self, validated_data):
        products_data = validated_data.pop('orderproduct_set')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)
        return order