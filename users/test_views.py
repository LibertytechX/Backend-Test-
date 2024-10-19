import pytest
from rest_framework.test import APIClient
from rest_framework import status
from users.views import CreateUserAPIView
from users.serializers import CreateUserSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def url():
    return "/api/v1/register"


@pytest.fixture
def serializer_class():
    return CreateUserSerializer


@pytest.mark.django_db
def test_create_user_with_invalid_data_returns_400(api_client, url, serializer_class):
    # Test with invalid data
    invalid_data = {
        "username": "",
        "email": "invalid_email",
        "password": "short",
    }
    response = api_client.post(url, invalid_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_with_missing_username_returns_400(
    api_client, url, serializer_class
):
    # Test with missing username
    data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_with_missing_email_returns_400(api_client, url, serializer_class):
    # Test with missing email
    data = {
        "username": "testuser",
        "password": "testpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_with_missing_password_returns_400(
    api_client, url, serializer_class
):
    # Test with missing password
    data = {
        "username": "testuser",
        "email": "test@example.com",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_with_existing_email_returns_400(api_client, url, serializer_class):
    # Test with existing email
    existing_user = {
        "username": "existinguser",
        "email": "existing@example.com",
        "password1": "Testpassword@123",
        "password2": "Testpassword@123",
    }
    api_client.post(url, existing_user, format="json")  # Create existing user

    data = {
        "username": "newuser",
        "email": "existing@example.com",
        "password1": "Testpassword@123",
        "password2": "Testpassword@123",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_success_returns_201(api_client, url):
    # Test with valid data
    data = {
        "username": "testuser1",
        "email": "test2@example.com",
        "password1": "Testpassword@123",
        "password2": "Testpassword@123",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


# Test for login endpoint


@pytest.fixture
def login_url():
    return "/api/v1/login"


@pytest.mark.django_db
def test_login_user_valid_data_returns_200(api_client, login_url, url):
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "Testpassword@123",
        "password2": "Testpassword@123",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    login_data = {
        "email": "test@example.com",
        "password": "Testpassword@123",
    }
    login_response = api_client.post(login_url, login_data, format="json")
    assert login_response.status_code == status.HTTP_200_OK
    assert login_response.data["data"]["access_token"] is not None


@pytest.mark.django_db
def test_login_user_bad_data_returns_400(api_client, login_url, url):
    """Test user login endpoint with invalid credentials"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "Testpassword@123",
        "password2": "Testpassword@123",
    }
    api_client.post(url, data, format="json")

    login_data = {
        "email": "test@example.com",
        "password": "Testpassword@",
    }
    login_response = api_client.post(login_url, login_data, format="json")
    assert login_response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid credentials" in login_response.data["message"]
