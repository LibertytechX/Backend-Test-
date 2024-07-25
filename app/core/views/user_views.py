
from rest_framework import generics
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from core.models import User
from core.serializers.user_serializers import CustomerSignUpSerializer, StaffSignUpSerializer, UserSerializer, MyTokenObtainPairSerializer


class CustomerRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSignUpSerializer


class StaffRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffSignUpSerializer

# login view


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# class ConfirmAccount(APIView):
#     def post(self, request):
#         data = request.data
#         token = data.get('token')
#         # print(data)
#         try:
#             # userToken = UserToken.objects.get(token=token)
#             # user = userToken.user
#             user.is_active = True
#             user.save()
#             return Response({"message": "Account Successfully Activated", "userId": user.id, "role": user.role, "name": user.name}, status=status.HTTP_201_CREATED)
#         except:
#             return Response({'message': 'Invalid Token,Kindly enter a valid Token.'}, status=status.HTTP_400_BAD_REQUEST)
