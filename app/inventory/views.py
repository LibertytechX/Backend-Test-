from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .custom_auth import EmailNameAuthBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db import transaction
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


#local imports
from .serializers import UserSerializer,ProductSerializer,\
    OrderItemSerializer,OrderSerializer,CategorySerializer,OrderHistorySerializer
from .models import Category, Product,Order,OrderItem
# Create your views here.


User = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):# serialize a JWT token combining user name and email
        token = super().get_token(user)
        token["name"] = user.name
        token["email"] = user.email
        
        return token

class CustomTokenObtain(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        data = request.data #get the request data and retrieve email/name and password
        name = data['email']or None
        password = data['password'] or None
        user = authenticate(request, email=name , password=password)# try to authenticate with the info
        if user is not None:# if user is authenticated and not none
            if user.is_active:
                refresh = RefreshToken.for_user(user) #get a refresh token
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token, status=status.HTTP_200_OK)# respond with the access and refresh token
            return Response({'error': 'Account disabled!'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Invalid login Details'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes =[]
    def post(self, request,*args,**kwargs):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer = serializer.save()

            data = {'message':f'Account created succesffuly!','data':UserSerializer(serializer).data}
            return Response(data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ProductView(APIView):#One View for all CRUD on Product model
    authentication_classes=[]
    permission_classes =[AllowAny]
    serializer_class = ProductSerializer #serializer class to be used all round the ProducView via self
    model_class = Product #model class to be used all round the ProducView via self
    def get(self, request, slug=None,*args,**kwargs):
        search_query = request.query_params.get('search', None)
        queryset = Product.objects.all()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
            paginator = PageNumberPagination()
            paginator.page_size = 1
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        if slug:
            try:
                product = self.model_class.objects.get(slug=slug)
                serializer = self.serializer_class(product,many =False)
                return Response(serializer.data)
            except self.model_class.DoesNotExist:
                return Response({'error':'Object not found!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            products = self.model_class.objects.all()
            serializer = self.serializer_class(products, many=True)
            for item in serializer.data:
                item['category'] = CategorySerializer(Category.objects.get(id = item['category'])).data
            return Response(serializer.data)

    def post(self, request,*args,**kwargs):
        data = request.data.copy()
        category_identifier =request.data.get('category','')
        category = Category.objects.filter(# get ctegory by Id or slug
                Q(slug__icontains=category_identifier) |Q(id__icontains=category_identifier))
        data['category'] = category[0].id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):
        try:
            product = self.model_class.objects.get(slug=slug)
        except self.model_class.DoesNotExist:# object not found
                return Response({'error':'Object not found!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            product = self.model_class.objects.get(slug=slug)
        except self.model_class.DoesNotExist:
                return  Response({'error':'Object not found!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)




class CategoryView(APIView):
    authentication_classes=[]
    permission_classes =[]
    serializer_class = CategorySerializer 
    model_class = Category
    def get(self, request, slug=None,*args,**kwargs):
        if slug:
            try:
                category = self.model_class.objects.get(slug=slug)
                serializer = self.serializer_class(category,many =False)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except self.model_class.DoesNotExist:
                return Response({'error':'Object not found!'}, status=status.HTTP_400_BAD_REQUEST)
        categories = self.model_class.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request,*args,**kwargs):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    permission_classes =[IsAuthenticated]
    serializer_class = OrderSerializer 
    model_class = Order
    def get(self, request, slug=None,*args,**kwargs):
        if slug:
            try:
                order = self.model_class.objects.get(slug=slug,user = request.user)
                serializer = OrderHistorySerializer(order,many =False)
                return Response(serializer.data)
            except self.model_class.DoesNotExist:
                return Response({'error':'Object not found!'}, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(user=request.user)
        serializer = OrderHistorySerializer(orders, many=True)
        return Response(serializer.data)

    @transaction.atomic #use atomic to rolback if need be
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            order = serializer.save()
            products_data = data.get('products', [])

            for item_data in products_data:
                try:
                    product = Product.objects.get(slug=item_data['slug'])
                    quantity = item_data.get('quantity', 1)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)
                except Product.DoesNotExist:
                    transaction.set_rollback(True)# rollback actions on db
                    return Response({'error': f"Product with slug {item_data['slug']} not found"}, status=status.HTTP_400_BAD_REQUEST)
    
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def endpoints(request):# endpoint to keep all out endpoint at the root url for easy access and development
    data = [
    
    "api/v1/register/", 
    "api/v1/token/", 
    "api/v1/token/refresh/", 
    #products urls
    'api/v1/inventory/products/',
    'api/v1/inventory/product/create/',
    'api/v1/inventory/product/<str:slug>/',
    'api/v1/inventory/product/<str:slug>/update/',
    'api/v1/inventory/product/<str:slug>/delete/',
    #category urls
    'api/v1/inventory/categories/',
    'api/v1/inventory/category/<str:slug>/',
    'api/v1/inventory/category/create/',
    #Order urls
    'api/v1/inventory/order/create/',
    'api/v1/inventory/order-history/',
    'api/v1/inventory/order/<str:slug>/history/',
]
    

    return Response(data)