from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Order, Product, Category, OrderProduct


class OrderTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="user@test.com", password='password')
        self.admin = User.objects.create_superuser(
            email="admin@test.com", password='password')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            price=1000.00,
            quantity=10,
            description='A high-performance laptop',
            category=self.category
        )

        self.place_order_url = reverse('create-order')
        self.order_list_url = reverse('order-list')
        # Use the actual order id if required
        self.order_detail_url = reverse('order-detail', args=[1])
        self.user_order_history_url = reverse('order-user-history')

    def test_place_order(self):
        data = {
            'products': [
                {'product_id': self.product.id, 'quantity': 5}
            ]
        }
        response = self.client.post(self.place_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)

    def test_place_order_no_products_data(self):
        response = self.client.post(self.place_order_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_place_order_invalid_products_data(self):
        data = {'products': 'invalid_data'}
        response = self.client.post(self.place_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_place_order_nonexistent_product(self):
        data = {
            'products': [
                {'product_id': 999, 'quantity': 5}
            ]
        }
        response = self.client.post(self.place_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_place_order_out_of_stock(self):
        data = {
            'products': [
                {'product_id': self.product.id, 'quantity': 15}
            ]
        }
        response = self.client.post(self.place_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_non_admin(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_admin(self):
        order = Order.objects.create(user=self.user)
        self.client.force_authenticate(user=self.admin)
        url = reverse('order-detail', args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_non_admin(self):
        order = Order.objects.create(user=self.user)
        url = reverse('order-detail', args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_order_history(self):
        order = Order.objects.create(user=self.user)
        response = self.client.get(self.user_order_history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
