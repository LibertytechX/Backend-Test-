from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationTest(APITestCase):

    def setUp(self):
        self.valid_payload = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'name': 'Test User'
        }
        self.invalid_payload = {
            'email': 'testuser@example.com',  # Duplicate email
            'password': 'testpassword123',
            'name': 'Test User'
        }

    def test_user_registration(self):
        response = self.client.post(reverse('registration'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User created successfully.')

    def test_user_registration_duplicate_email(self):
        self.client.post(reverse('registration'), data=self.valid_payload)
        response = self.client.post(reverse('registration'), data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login(self):
        self.client.post(reverse('registration'), data=self.valid_payload)
        login_payload = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('login'), data=login_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        self.client.post(reverse('registration'), data=self.valid_payload)
        login_payload = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data=login_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
