from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from ..shop.models import Product
from .serializers import ProductSerializer
from ..cart.cart import Cart


class ProductListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(owner=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {
            'category': request.data.get('category'),
            'name': request.data.get('name'),
            'slug': request.data.get('slug'),
            'image': request.data.get('image'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'available': request.data.get('available'),
            'owner': request.user.id 
        }
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, request, name, slug):
        return get_object_or_404(Product, name=name, slug=slug)

    def get(self, request, name, slug):
        product_instance = self.get_object(name, slug)
        self.check_object_permissions(request, product_instance)
        serializer = ProductSerializer(product_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, name, slug, *args, **kwargs):
        product_instance = self.get_object(name, slug)
        self.check_object_permissions(request, product_instance)
        data = {
            'name': request.data.get('name'),
            'slug': request.data.get('slug'),
            'price': request.data.get('price'),
            'available': request.data.get('available'),
            'description': request.data.get('description')
        }
        serializer = ProductSerializer(instance=product_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, slug):
        product_instance = self.get_object(name, slug)
        self.check_object_permissions(request, product_instance)
        product_instance.delete()
        return Response(
            {"res": "Product deleted"},
            status=status.HTTP_200_OK
        )


class CartAddView(APIView):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity', 1)
        override_quantity = request.data.get('override', False)
        cart.add(product, quantity, override_quantity)
        return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)


class CartRemoveView(APIView):
    def delete(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return Response({'message': 'Product removed from cart'}, status=status.HTTP_200_OK)


class CartDetailView(APIView):
    def get(self, request):
        cart = Cart(request)
        cart_items = list(cart)
        total_price = cart.get_total_price()
        return Response({'cart_items': cart_items, 'total_price': total_price}, status=status.HTTP_200_OK)


class CartClearView(APIView):
    def delete(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_200_OK)
