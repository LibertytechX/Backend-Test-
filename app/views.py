from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework import status
from store.models import *
from .utils import *


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """
    The `register_user` function takes a request, validates the user data using a serializer, saves the
    user if valid, and returns the appropriate response.

    :param request: The `request` parameter in the `register_user` function is typically an HTTP request
    object that contains data sent by the client to the server. This data can include information such
    as user input, headers, cookies, and other relevant details needed to process the request. In this
    context, it seems like
    :return: If the serializer is valid, the user data will be saved and a response with the user data
    and status code 201 (Created) will be returned. If the serializer is not valid, a response with the
    serializer errors and status code 400 (Bad Request) will be returned.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    The `login` function takes a request, validates the login credentials using a serializer,
    authenticates the user, and returns access and refresh tokens if the credentials are valid.

    :param request: The `login` function you provided seems to be a view function in a Django REST
    framework API for handling user authentication. It takes a `request` object as a parameter, which
    typically contains data sent by the client making the request
    :return: The `login` function returns a response based on the validation of the `LoginSerializer`
    data and the authentication of the user. If the serializer data is valid and the user is
    authenticated successfully, it returns a response containing a refresh token and an access token. If
    the user is not authenticated (invalid credentials), it returns a response with a message indicating
    "Invalid credentials" and a status code of
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.data["email"], password=serializer.data["password"]
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### CRUD operations for Products


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_product(request):
    """
    The function `create_product` takes a request, validates the data using a serializer, saves the data
    if valid, and returns the serialized data with appropriate status codes.

    :param request: The `request` parameter in the `create_product` function is typically an object that
    contains information about the incoming HTTP request, such as the data being sent in the request
    body. In this case, it seems like the `request` parameter is being used to create a new product by
    serializing the
    :return: If the serializer is valid, the function will return the serialized data with a status of
    HTTP 201 Created. If the serializer is not valid, it will return the serializer errors with a status
    of HTTP 400 Bad Request.
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_products(request):
    search_query = request.query_params.get("search", None)
    query_products = Product.objects.all()
    if search_query:
        products = query_products.filter(name__icontains=search_query)

    paginator = ProductPagination()
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def getProductDetail(request):
    query_product = Product.objects.get(pk=request.data.get("Id"))
    serializer = ProductSerializer(query_product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_product(request, pk):
    try:
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_product(request):
    """
    The `delete_product` function deletes a product based on the provided ID in a Django REST framework
    view.

    :param request: The `delete_product` function is designed to handle a request to delete a product
    from a database. It expects the request object to contain data with a key "Id" that represents the
    ID of the product to be deleted
    :return: The `delete_product` function is returning a response based on the outcome of the deletion
    operation:
    """
    try:
        product_id = request.data.get("Id")
        if not product_id:
            return Response(
                {"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        product = Product.objects.get(pk=product_id)
        product.delete()
        return Response("Successfully deleted!", status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_order(request):
    """
    The function `create_order` takes a request, validates the data using an `OrderSerializer`, assigns
    the user to the order, and returns a response with the appropriate status code.

    :param request: The `request` parameter in the `create_order` function is typically an object that
    contains information about the incoming HTTP request, such as the request method, headers, body, and
    user authentication details. In this context, it seems to be used to create a new order by
    serializing the data from
    :return: If the serializer is valid, the function will return the serialized data with a status of
    HTTP 201 Created. If the serializer is not valid, it will return the serializer errors with a status
    of HTTP 400 Bad Request.
    """
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        instance.for_user = request.user
        instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def getOrderHistory(request):
    """
    This function retrieves order history for a specific user and returns it in a serialized format.

    :param request: The `request` parameter in the `getOrderHistory` function is typically an HTTP
    request object that contains information about the current request, including user authentication
    details, query parameters, and other request data. In this context, it seems like the function is
    expected to retrieve order history for a specific user based
    :return: The `getOrderHistory` function returns a Response object with the serialized data of orders
    if the serializer is valid, along with a status of HTTP 200 OK. If the serializer is not valid, it
    returns an empty data object with a status of HTTP 400 BAD REQUEST.
    """
    if request.user:
        orders = Order.objects.filter(for_user_id=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Not a logged in user"}, status=status.HTTP_404_NOT_FOUND
        )
