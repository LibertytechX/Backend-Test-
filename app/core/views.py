from .models import User
from .serializers import UserSerializer, FavouriteSerializer, CoinsSerializer
from .models import User, Coins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


# CREATE NEW USER VIA API
class CreateUser(generics.CreateAPIView):
    '''
    URL:
    http://127.0.0.1:8000/register/

    USING CURL COMMAND:
    curl --data "email=ben@gmail.com&username=ben&password=1234" http://127.0.0.1:8000/register/

    USING PYTHON REQUESTS:
    import requests
    url = 'http://127.0.0.1:8000/register/'
    data = {'email': 'fred@gmail.com', 'username': 'Fred', 'password': 1234}
    response = requests.post(url, data=data)
    print(response.text)

    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Created user successfully',
            'username': response.data['username'],
            'status': 200,
                  })
    

# GET ALL COINS
class GetCoins(generics.ListAPIView):
    '''
    URL:
    http://127.0.0.1:8000/getcoins/

    USING CURL COMMAND:
    curl http://127.0.0.1:8000/getcoins/

    USING PYTHON REQUESTS:
    import requests
    url = 'http://127.0.0.1:8000/getcoins/'
    response = requests.get(url)
    print(response.text)

    '''

    serializer_class = CoinsSerializer
    queryset = Coins.objects.all()


# ADD FAVOURITES VIA API
class AddFavourite(generics.CreateAPIView):
    '''
    REMARKS:
    ID of user and ID of coin must be provided

    URL:
    http://127.0.0.1:8000/addfavourite/

    USING CURL COMMAND:
    curl --data "favourite=45&user=3" http://127.0.0.1:8000/addfavourite/

    USING PYTHON REQUESTS:
    import requests
    url = 'http://127.0.0.1:8000/addfavourite/'
    data = {'favourite': 45, 'user': 4}
    response = requests.post(url, data=data)
    print(response.text)

    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = FavouriteSerializer(data=request.data)
                
        if serializer.is_valid():

            # GRAB COIN NAME TO BE INCLUDED IN RESPONSE
            coin_id = serializer.validated_data['favourite'].id
            coin_name = Coins.objects.get(id = coin_id).name
            
            # GRAB USERNAME TO BE INCLUDED IN RESPONSE
            user_id = serializer.validated_data['user'].id
            username = User.objects.get(id = user_id).username

            serializer.save()
            
            return Response({
            'message': 'Added {} to favourite successfully'.format(coin_name),
            'username': '{}'.format(username),
            'coin_name': coin_name,
            'status': 200,
                  })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# VIEW FAVOURITES FOR SPECIFIC USER
class ViewFavourites(generics.ListAPIView):
    '''
    REMARKS:
    ID of user must be included at end of url as a parameter

    URL:
    http://127.0.0.1:8000/viewfavourites/?userid=1

    USING CURL COMMAND:
    curl http://127.0.0.1:8000/viewfavourites/?userid=1

    USING PYTHON REQUESTS:
    import requests
    url = 'http://127.0.0.1:8000/viewfavourites/?userid=1'
    response = requests.get(url)
    print(response.text)
    
    '''
    serializer_class = UserSerializer  
    
    def get_queryset(self):
        user_id = self.request.query_params.get('userid')
        queryset = User.objects.filter(id = user_id)
        return queryset


# CREATE COINS VIA API (MANAGEMENT COMMANDS) TO SEED DATABASE
class LoadDB(generics.CreateAPIView):
    '''
    REMARKS:
    This is only required at project initiation

    Management command used to load the db
    URL: 'http://127.0.0.1:8000/loaddb/'
    '''
    queryset = Coins.objects.all()
    serializer_class = CoinsSerializer