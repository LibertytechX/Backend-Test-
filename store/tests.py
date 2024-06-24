from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItem, Category


class ProductModelTests(TestCase):
    """Test product and category model creations."""

    def test_create_category_successful(self):
        """Test creating a new category is successful."""
        name = "Electronics"
        category = Category.objects.create(name=name)

        self.assertEqual(category.name, name)

    def test_create_product_successful(self):
        """Test creating a new product is successful."""
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Laptop",
            category=category,
            price=999.99,
            description="A high-end gaming laptop.",
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.category.name, "Electronics")
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.description, "A high-end gaming laptop.")


# Order Test
class OrderModelTests(TestCase):
    """Test order model creations and management."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpassword123"
        )
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.category = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(
            name="Laptop",
            category=self.category,
            price=999.99,
            description="A high-end gaming laptop.",
        )
        self.product2 = Product.objects.create(
            name="Smartphone",
            category=self.category,
            price=699.99,
            description="A flagship smartphone.",
        )

    def test_place_order(self):
        """Test placing an order is successful."""
        payload = {
            "items": [
                {"product": self.product1.id, "quantity": 1},
                {"product": self.product2.id, "quantity": 2},
            ]
        }
        response = self.client.post("api/create-order/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)

    def test_order_history(self):
        """Test retrieving order history for the authenticated user."""
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product1, quantity=1)
        OrderItem.objects.create(order=order, product=self.product2, quantity=2)

        response = self.client.get("api/order-history/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]["items"]), 2)
        self.assertEqual(response.data[0]["items"][0]["product"], self.product1.id)
        self.assertEqual(response.data[0]["items"][1]["product"], self.product2.id)
