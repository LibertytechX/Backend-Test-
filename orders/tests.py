import pytest
from rest_framework.test import APIClient
from products.models import Category, Product
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def url():
    return "/api/v1/orders"


@pytest.mark.django_db
def test_place_order_returns_201(api_client, url):
    # create user
    user = User.objects.create_user(
        username="TestUser", password="TestPassword", email="testuser@test.com"
    )
    api_client.force_authenticate(user=user)
    # create a product
    cat = Category.objects.create(name="Test Category")
    product = Product.objects.create(
        category=cat,
        name="Iphone 12",
        available_quantity=20,
        price=2000000,
        discount_price=190000,
        description="some description",
    )
    # Test with valid data
    data = {"products": [{"product_id": product.id, "quantity": 2}]}
    response = api_client.post(f"{url}/place", data, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_place_order_returns_400_when_product_not_found(api_client, url):
    # create user
    user = User.objects.create_user(
        username="TestUser", password="TestPassword", email="testuser@test.com"
    )
    api_client.force_authenticate(user=user)
    # Test with invalid product_id
    data = {"products": [{"product_id": 1000, "quantity": 2}]}
    response = api_client.post(f"{url}/place", data, format="json")
    assert response.status_code == 400
    assert f"Product 1000 not found" in response.json()["message"]


@pytest.mark.django_db
def test_order_history_returns_200(api_client, url):
    user = User.objects.create_user(
        username="TestUser", password="TestPassword", email="testuser@test.com"
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
