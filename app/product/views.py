from rest_framework.views import APIView
from app.modules.utils import incoming_request_checks
from product.models import Product
from product.serializers import ProductSerializerOut
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.modules.exceptions import raise_serializer_error_msg
from app.modules.utils import api_response, get_incoming_request_checks, incoming_request_checks
# from app.modules.permissions import IsAgentAdmin, IsAdmin
from app.modules.paginations import TenInPagePagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import CartItemSerializer, CartSerializer, CreateOrderSerializer, OrderItemSerializer, OrderSerializer, ProductSerializerIn, ProductSerializerOut
from .models import Cart, Cartitems, Order, OrderItems, Product, Color 
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdminUser)]

    serializer_class = ProductSerializerOut
    
    def dispatch(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.http_method_names = ['get', 'put', 'patch', 'delete']
        else:
            self.http_method_names = ['get', 'post']
        
        return super().dispatch(request, *args, **kwargs)
        
            
    def get_queryset(self):
        return Product.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return super().get_permissions()

    def update(self, request, pk, partial=False, format=None):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializerIn(instance, data=data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        link = serializer.save()
        return Response(
            api_response(
                message="Product updated successfully", status=True, data=link
            )
        )

    def get(self, request, pk=None, format=None):
        if pk:
            instance = get_object_or_404(Product, pk=pk)
            serializer = self.serializer_class(instance)
            return Response(
                api_response(
                    message="Product retrieved successfully",
                    status=True,
                    data=serializer.data,
                )
            )
        else:
            category = request.query_params.get('category', None)
            search = request.query_params.get('search', None)
            if category:
                if category == 'popular':
                    queryset = self.get_queryset().order_by('-number_sold')
                elif category == 'lowest':
                    queryset = self.get_queryset().order_by('amount')
                elif category == 'highest':
                    queryset = self.get_queryset().order_by('-amount')
                else:
                    queryset = self.get_queryset().filter(category__title=category)
            else:
                queryset = self.get_queryset()
            if search:
                
                colors = Color.objects.filter(color__icontains=search)
                queryset = queryset.distinct().filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search) |
                    Q(category__name__icontains=search) |
                    Q(price__icontains=search) |
                    Q(colors__in=colors)
                )
        
            paginator = TenInPagePagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(paginated_queryset, many=True)
            data = paginator.get_paginated_response(serializer.data)          
            message = "Products retrieved successfully" if len(serializer.data) > 0 else "No product available"
            return Response(
                api_response(
                    message=message,
                    status=True,
                    data=data.data,
                )
            )

    def post(self, request, format=None):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ProductSerializerIn(data=data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        data = serializer.save()
        return Response(
            api_response(
                message="Product created successfully", status=True, data=data
            ),
            status=status.HTTP_201_CREATED
        )

    def put(self, request, pk, format=None):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializerIn(instance, data=data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        link = serializer.save()
        return Response(
            api_response(
                message="Product updated successfully", status=True, data=link
            )
        )

    def patch(self, request, pk, format=None):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializerIn(instance, data=data, partial=True)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        data = serializer.save()
        return Response(
            api_response(
                message="Product updated successfully", status=True, data=data
            )
        )

    def delete(self, request, pk, format=None):
        instance = get_object_or_404(Product, pk=pk)
        instance.delete()
        return Response(
            api_response(message="Product deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT,
        )


class CartView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Cart.objects.filter(owner=self.request.user).first()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
                api_response(
                    message="Cart retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    

class CartItemView(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
    def get_object(self):
        cartitem = get_object_or_404(Cartitems, id=self.kwargs['pk'])
        return cartitem
    
    
    def list(self, request, *args, **kwargs):
        queryset = Cart.objects.filter(owner=self.request.user).first()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CartSerializer()
            return self.get_paginated_response(serializer.data)

        serializer = CartSerializer(queryset)
        return Response(
                api_response(
                    message="Cart retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
        
    def create(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
                api_response(
                    message="Cartitem added successfully",
                    status=True,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
                api_response(
                    message="Cartitem retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def update(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(instance)
        serializer = self.serializer_class(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message="Cartitem updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message="Cartitem deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )
    

class OrderView(ListModelMixin,
                CreateModelMixin,
                RetrieveModelMixin,
                GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
                api_response(
                    message="User Orders Retrieved successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def create(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
                api_response(
                    message="Order retreived successfully",
                    status=True,
                    data=order,
                )
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
                api_response(
                    message="Order retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(owner=user)
    
    
class VerifyOrder(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        order = get_object_or_404(Order, id=pk)
        serializer = OrderSerializer(order)
        order.verified()
        print(serializer.data)
        return Response(
            api_response(
                message="Order verified successfully", status=True, data=serializer.data
            )
        )


    
    
    