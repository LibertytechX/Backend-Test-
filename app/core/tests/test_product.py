from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, Category, Product

class ProductTests(APITestCase):

    def setUp(self):
        self.client.post(reverse('register'), {"email": 'user@example.com', "password": 'password123', "name": "test", "is_active": True})
        self.client.post(reverse('register'), {"email": 'staff@example.com', "password": 'password123', "name": "test", "is_staff": True, "is_active": True})
        auth_res = self.client.post(reverse('login'), {"email": 'user@example.com', "password": 'password123'})
        self.user_token = auth_res.data["token"]["access"]
        auth_res = self.client.post(reverse('login'), {"email": 'staff@example.com', "password": 'password123'})
        self.staff_token = auth_res.data["token"]["access"]
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(name='Product1', price=10.00, category=self.category)

    def test_list_products(self):
        url = reverse('products')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.user_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        url = reverse('products')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.staff_token)
        data = {
            'name': 'Product2',
            'price': 20.00,
            'categoryId': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        url = reverse('product', args=[self.product.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.user_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)

    def test_update_product(self):
        url = reverse('product', args=[self.product.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.staff_token)
        data = {
            'name': 'UpdatedProduct',
            'price': 30.00,
            'categoryId': self.category.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'UpdatedProduct')
        self.assertEqual(self.product.price, 30.00)

    def test_delete_product(self):
        url = reverse('product', args=[self.product.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.staff_token)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
