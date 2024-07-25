import json
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Order, Product, OrderProduct
from core.serializers.order_serializers import OrderSerializer, OrderDetailSerializer


class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        products_data = request.data.get('products')

        if not products_data:
            return Response({"error": "Products data is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(products_data, list):
            return Response({"error": "Products data must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        out_of_stock = []
        quantity_exceeded = []

        order = Order.objects.create(user=user)

        for product_data in products_data:
            if not isinstance(product_data, dict):
                return Response({"error": "Each product data must be a dictionary"}, status=status.HTTP_400_BAD_REQUEST)

            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity')

            if product_id is None or quantity is None:
                return Response({"error": "Product data must include 'product_id' and 'quantity'"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": f"Product with id {product_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if product.quantity >= quantity:
                current_quantity = product.quantity - quantity
                product.quantity = current_quantity
                OrderProduct.objects.create(
                    order=order, product=product, quantity=quantity)
                product.save()
            else:
                if product.quantity < 1:
                    out_of_stock.append(product_id)
                else:
                    quantity_exceeded.append(product_id)

        if out_of_stock:
            message = {"message": "Some products are out of stock",
                       "product_ids": out_of_stock}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        if quantity_exceeded:
            message = {"message": "Some product quantities exceeded available stock",
                       "product_ids": quantity_exceeded}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class OrderGetView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class OrderUserHistoryView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
