from django.test import TestCase
from core.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_create_url = reverse('register')
        self.logout_url = reverse('auth_logout')
        self.user = User.objects.create_user(email='test@example.com', password='Test@pass123')

    def test_user_creation(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'Newpass@123',
        }
        response = self.client.post(self.user_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['message'], 'User Created Successfully')
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_creation_invalid_data(self):
        data = {
            'email': 'invalid-email',
            'password': 'short',
            
        }
        response = self.client.post(self.user_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        data = {'refresh': str(refresh)}
        response = self.client.post(self.logout_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['message'], 'User logged out successfully')

    def test_user_creation_duplicate_email(self):
        data = {
            'email': 'test@example.com',  # This email already exists
            'password': 'Newpass@123',
            
        }
        response = self.client.post(self.user_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
