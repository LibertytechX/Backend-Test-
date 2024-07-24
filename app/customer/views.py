from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from app.modules.utils import api_response, incoming_request_checks
from customer.models import CustomerDetail
from customer.serializers import CreateUserSerializer, CreateUserSerializerOut, CustomerSerializer, LoginSerializerIn
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated


class CustomersView(CreateModelMixin, RetrieveModelMixin,
                    UpdateModelMixin, GenericAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method not in ['PATCH', 'PUT', 'GET']:
            return []
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return super().get_serializer_class()
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id}
    
    def get_object(self):
        user_id = self.request.user.id
        customerdetail, _= CustomerDetail.objects.get_or_create(user_id=user_id)
        return customerdetail
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
                api_response(
                    message="User retreived successfully",
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
        user = serializer.save()
        print(user)
        return Response(
                api_response(
                    message="User retreived successfully",
                    status=True,
                    data=user,
                ),
             status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        partial = kwargs.pop('partial', False)
        if self.request.method == "PATCH":
            partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message="User updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    

class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = LoginSerializerIn(data=data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            api_response(
                message="Login successfully",
                status=True,
                data={
                    "accessToken": f"{AccessToken.for_user(user)}",
                    "refreshToken": f"{RefreshToken.for_user(user)}",
                }
            )
        )
    
    