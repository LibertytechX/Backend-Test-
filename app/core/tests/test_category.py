from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, Category

class CategoryTests(APITestCase):

    def setUp(self):
        self.client.post(reverse('register'), {"email": 'user@example.com', "password": 'password123', "name": "test", "is_active": True})
        self.client.post(reverse('register'), {"email": 'staff@example.com', "password": 'password123', "name": "test", "is_staff": True, "is_active": True})
        auth_res = self.client.post(reverse('login'), {"email": 'user@example.com', "password": 'password123'})
        self.user_token = auth_res.data["token"]["access"]
        auth_res = self.client.post(reverse('login'), {"email": 'staff@example.com', "password": 'password123'})
        self.staff_token = auth_res.data["token"]["access"]
        self.category = Category.objects.create(name='TestCategory')

    def test_list_categories(self):
        url = reverse('categories')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        url = reverse('categories')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        data = {
            'name': 'NewCategory'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_retrieve_category(self):
        url = reverse('category', args=[self.category.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.category.id)

    def test_update_category(self):
        url = reverse('category', args=[self.category.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        data = {
            'name': 'UpdatedCategory'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'UpdatedCategory')

    def test_delete_category(self):
        url = reverse('category', args=[self.category.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
