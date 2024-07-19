from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User

class UserTests(APITestCase):

    def setUp(self):
        self.client.post(reverse('register'), {"email": 'user@example.com', "password": 'password123', "name": "test", "is_active": True})
        self.client.post(reverse('register'), {"email": 'staff@example.com', "password": 'password123', "name": "test", "is_staff": True, "is_active": True})
        auth_res = self.client.post(reverse('login'), {"email": 'user@example.com', "password": 'password123'})
        self.user_token = auth_res.data["token"]["access"]
        auth_res = self.client.post(reverse('login'), {"email": 'staff@example.com', "password": 'password123'})
        self.staff_token = auth_res.data["token"]["access"]
    
    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'name': "test"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_user(self):
        url = reverse('login')
        data = {
            'email': 'user@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user@example.com')
