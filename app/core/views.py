from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.conf import settings

API_KEY = settings.API_KEY
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import RegistrationSerializer, AssetsListSerializer, AddCoinActionSerializer, AddCoinSerializer, \
    AddViewSerializer
from rest_framework.authtoken.models import Token
import requests
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import serializers

from .models import Favourite, User, Coin, Favourite
from rest_framework import generics

import json


@api_view(['POST'])
def registeration_view(request, *args, **kwargs):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['message'] = "Created user successfully"
        data['full_name'] = account.full_name
        data['email'] = account.email
        token = Token.objects.get(user=account).key
        data['token'] = token
        return Response(data, status=201)
    data = serializer.errors
    return Response(data, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assets_listView(request, *args, **kwargs):
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': API_KEY}
    response = requests.get(url, headers=headers)
    re = response.json()
    data = []
    print('re : ' + str(re))
    index = 0
    for i in re:
        print('i : ' + str(i))
        dict = {
            "name": i["name"],
            "volume": i["volume_1hrs_usd"]
        }
        data.append(dict)  # ADDING DICTIONARY TO PARENT DICTIONARY
        index = index + 1
    print(type(re))
    serializer = AssetsListSerializer(data=data, many=True)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=200)
    return Response({}, status=404)


@api_view(['GET', 'POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def add_coin_to_fav(request, *args, **kwargs):
    serializer = AddCoinActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        coin_id = data.get("id")
        action = data.get("action")
        id = Coin.objects.filter(id=coin_id)
        obj = id.first()
        #if in the database????
        if obj:
            favourite, created = Favourite.objects.get_or_create(
                user=request.user,
            )
            # action are "add" or "remove"
            if action == "add":
                if obj in favourite.coin.all():
                    serializer = AddCoinSerializer(obj)
                    json_response = {}
                    json_response["message"] = F"hi {request.user.full_name} {obj} Already  in favourite",
                    json_response["coin"] = serializer.data
                    return Response(json_response, status=200)
                favourite.coin.add(obj)
                serializer = AddCoinSerializer(obj)
                json_response = {}
                json_response["message"] = "Added {} to favourite successfully".format(obj),
                json_response["username"] = request.user.full_name,
                json_response["coin"] = serializer.data
                return Response(json_response, status=201)
            elif action == "remove":
                favourite.coin.remove(obj)
                serializer = AddCoinSerializer(obj)
                json_response = {}
                json_response["message"] = "removed {} to favourite successfully".format(obj),
                json_response["username"] = request.user.full_name,
                json_response["coin"] = serializer.data
                return Response(json_response, status=200)
        return Response({"Not found"}, status=404)
    return Response({}, status=400)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 4
    paginated_qs = paginator.paginate_queryset(qs, request, )
    user = request.user
    json_response = {}
    serializer = AddViewSerializer(paginated_qs, many=True)
    json_response["message"] = F"Welcome back {user.full_name} thanks for using our platform"

    json_response["subscribed_favourites"] = serializer.data

    return paginator.get_paginated_response(json_response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fav_view(request, *args, **kwargs):
    qs = Favourite.objects.filter(user=request.user)
    if qs:
        qs = qs[0]
        data = qs.coin.all()
        return get_paginated_queryset_response(data, request)
    json_response = {}
    json_response["message"] = F"No coin in your favourite, please add coin"
    return Response(json_response, status=404)