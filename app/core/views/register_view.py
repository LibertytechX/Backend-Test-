from rest_framework.generics import CreateAPIView
from rest_framework import status

from core.models import User
from core.serializers.register_serializer import RegisterSerializer
from lib.response import Response


# Create your view(s) here.
class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            serializer.save()

            return Response(data={
                'message': 'Created user succesfully',
                'username': username
            }, status=status.HTTP_200_OK)
