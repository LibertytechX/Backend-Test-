from core.models import User
from django.urls import reverse
from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.


class UserTests(APITestCase):
    def test_create_user_endpoint(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('signup')
        data = {
            'email': 'testuser@example.com',
            'name':'mike',
            'password1':'mystrongpassword123',
            'password2':'mystrongpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'mike')

 
    def test_jwt_login_endpoint(self):
        """
        Ensure we can login with JWT.
        """
        user = User.objects.create_user(email='testuser@gmail.com', name='mike', password='testpassword')
        url = reverse('login')
        data = {
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)




