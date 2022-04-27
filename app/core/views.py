from rest_framework.response import Response
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.decorators import api_view


# Register users

@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            # Response message
            return Response(
                {
                    "message": "Created user successfully",
                    "username": user_serializer.data.get('name'),
                    "status": 200
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Message": "Use a post request"}, status=status.HTTP_400_BAD_REQUEST)