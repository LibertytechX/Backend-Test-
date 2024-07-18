from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.exceptions import InvalidRequestException
from core.models import User, ProductCategory, Product, OrderDetail, Order


class UserSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "is_superuser", "groups", "user_permissions", "last_login"]


class SignUpSerializerIn(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        name = validated_data.get("name")
        email = validated_data.get("email")
        password = validated_data.get("password")

        if User.objects.filter(email__iexact=email).exists():
            raise InvalidRequestException({"detail": "User with this email already exist"})

        # Create user
        user = User.objects.create_user(email=email, password=password)
        user.name = name
        user.save()

        return "Account created successfully"


class LoginSerializerIn(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise InvalidRequestException({"detail": "Invalid email or password"})

        return user


class ProductCategorySerializerOut(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = []


class ProductSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []
        depth = 1


class ProductSerializerIn(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=200, required=False)
    price = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    category_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        name = validated_data.get("name")
        narration = validated_data.get("description")
        price = validated_data.get("price")
        cat_id = validated_data.get("category_id")

        if not all([name, narration, price, cat_id]):
            raise InvalidRequestException({"detail": "Required fields [name, description, price, category_id]"})

        try:
            category = ProductCategory.objects.get(id=cat_id)
        except ProductCategory.DoesNotExist:
            raise InvalidRequestException({"detail": "Selected product category is NOT valid"})

        product = Product.objects.create(name=name, description=narration, price=price, category=category)
        return ProductSerializerOut(product).data

    def update(self, instance, validated_data):
        cat_id = validated_data.get("category_id")

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        if cat_id:
            category = get_object_or_404(ProductCategory, id=cat_id)
            instance.category = category
        instance.save()
        return ProductSerializerOut(instance).data


class OrderSerializerOut(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.id")
    user_name = serializers.CharField(source="user.name")
    order_detail = serializers.SerializerMethodField()

    def get_order_detail(self, obj):
        if obj.order_detail:
            return [{"id": item.id, "quantity": item.quantity, "product_name": item.product.name, "total_price": item.total_price} for item in obj.order_detail.all()]

    class Meta:
        model = Order
        exclude = ["user"]


class OrderPlacementSerializerIn(serializers.Serializer):
    """
    This serializer is aimed to accept a list of order details in below format, use create an order with data
    order_request = [
        {
            "product_id": 1,
            "quantity": 10
        },
        {
            "product_id": 2,
            "quantity": 5
        }
    ]
    """
    order_request = serializers.ListSerializer(child=serializers.DictField())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data.get("user")
        order_placement = validated_data.get("order_request")

        # Create order detail for each request
        order_list = list()
        for prod in order_placement:
            if prod["product_id"] and prod["quantity"]:
                product_id = prod["product_id"]
                quantity = prod["quantity"]
                try:
                    product = Product.objects.get(id=product_id)
                    order_price = float(product.price) * quantity
                    # Create OrderDetail
                    order_detail = OrderDetail.objects.create(product=product, quantity=quantity, total_price=order_price)
                    order_list.append(order_detail.id)
                except Product.DoesNotExist:
                    # Log product does not exit
                    pass

        if order_list:
            # Create Order
            order = Order.objects.create(user=user)
            for od in order_list:
                order.order_detail.add(od)
            data = OrderSerializerOut(order).data
            return {"detail": "Order created successfully", "data": data}

        else:
            raise InvalidRequestException({
                "detail": "No order was created (this can be due to incorrect payload or no item found for placement)"
            })







