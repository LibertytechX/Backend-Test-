from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, Category, Product, Order, OrderItem

class OrderTests(APITestCase):

    def setUp(self):
        self.client.post(reverse('register'), {"email": 'user@example.com', "password": 'password123', "name": "test", "is_active": True})
        self.client.post(reverse('register'), {"email": 'staff@example.com', "password": 'password123', "name": "test", "is_staff": True, "is_active": True})
        auth_res = self.client.post(reverse('login'), {"email": 'user@example.com', "password": 'password123'})
        self.user_token = auth_res.data["token"]["access"]
        auth_res = self.client.post(reverse('login'), {"email": 'staff@example.com', "password": 'password123'})
        self.staff_token = auth_res.data["token"]["access"]
        self.category = Category.objects.create(name='TestCategory')
        self.product1 = Product.objects.create(name='Product1', price=10.00, category=self.category)
        self.product2 = Product.objects.create(name='Product2', price=20.00, category=self.category)
        self.user = User.objects.get(id=auth_res.data["user"]["id"])
        self.order = Order.objects.create(user=self.user)
        self.order_item1 = OrderItem.objects.create(order=self.order, product=self.product1, quantity=1, price=10.00)
        self.order_item2 = OrderItem.objects.create(order=self.order, product=self.product2, quantity=2, price=40.00)

    def test_create_order(self):
        url = reverse('orders')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.staff_token)
        data = {
            "items": [
                {"productId": self.product1.id, "quantity": 2},
                {"productId": self.product2.id, "quantity": 1}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(OrderItem.objects.count(), 4)

    def test_list_orders_as_staff(self):
        url = reverse('orders')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.staff_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_orders_as_user(self):
        url = reverse('orders')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.staff_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_order(self):
        url = reverse('order', args=[self.order.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.staff_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)

    def test_update_order(self):
        url = reverse('order', args=[self.order.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.staff_token)
        data = {
            "items": [
                {"productId": self.product1.id, "quantity": 3}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.items.first().quantity, 3)

    def test_delete_order(self):
        url = reverse('order', args=[self.order.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.staff_token)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())
