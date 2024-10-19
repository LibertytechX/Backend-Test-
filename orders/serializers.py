from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Order, OrderProduct
from products.models import Product


class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ["product_id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ["user", "products", "created_at", "status", "order_ref"]

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        # TODO: refactor to handle product that doesn't exist

        for product_data in products_data:
            try:
                product = Product.objects.get(
                    id=int(product_data["product_id"]))
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Product {product_data['product_id']} not found")
            # TODO: check product inventory if in sto
            OrderProduct.objects.create(
                order=order, product=product, quantity=product_data["quantity"]
            )
        order.calculate_total_amount()
        return order


class OrderProductListSerializer(ModelSerializer):
    product_id = serializers.IntegerField(source="product.id")
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", read_only=True, max_digits=10, decimal_places=2
    )
    # quantity = serializers.IntegerField()
    subtotal = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = OrderProduct
        fields = ["product_id", "product_name",
                  "product_price", "quantity", "subtotal"]
        read_only_fields = ["subtotal"]


class OrderListSerializer(ModelSerializer):
    order_products = OrderProductListSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            "user",
            "order_products",
            "created_at",
            "status",
            "order_ref",
            "total_amount",
        ]
