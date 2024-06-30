from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Order,OrderItem
from product.models import Product,Category

User = get_user_model()


class OrderViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpass')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A high-end laptop',
            price=1200.00,
            category=self.category
        )
        self.order = Order.objects.create(user=self.user, paid=True)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        self.valid_payload = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 1
                }
            ]
        }
        self.invalid_payload = {
            'items': [
                {
                    'product': 999,  # Assuming this product ID doesn't exist
                    'quantity': 1
                }
            ]
        }

        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_order_list_authenticated(self):
        response = self.client.get(reverse('order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one order is returned

    def test_get_order_list_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.get(reverse('order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_authenticated(self):
        response = self.client.post(
            reverse('order-list-create'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.post(
            reverse('order-list-create'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_with_invalid_product(self):
        response = self.client.post(
            reverse('order-list-create'),
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_order_detail_authenticated(self):
        response = self.client.get(reverse('order-detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.pk)

    def test_get_order_detail_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.get(reverse('order-detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_detail_not_owner(self):
        new_user = User.objects.create_user(email='newuser', password='newpass')
        refresh = RefreshToken.for_user(new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.get(reverse('order-detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

