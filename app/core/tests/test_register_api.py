from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


# Create your test(s) here.
class TestRegisterAPI(TestCase):
    def setUp(self):
        """Set up server client"""
        self.client = APIClient()

    def test_api_create_user_account(self):
        """Test register user account"""
        data = {
            'email': 'teiker@libertymail.com',
            'username': 'way2teiker',
            'password': 'Solarizedgowns'}

        response = self.client.post(
            reverse('register'),
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_api_email_field_may_not_be_blank(self):
        """Test email field may not be blank"""
        data = {
            'email': '',
            'username': 'way2teiker',
            'password': 'Solarizedgowns'}

        response = self.client.post(
            reverse('register'),
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_api_username_field_may_not_be_blank(self):
        """Test username field may not be blank"""
        data = {
            'email': 'teiker@libertymail.com',
            'username': '',
            'password': 'Solarizedgowns'}

        response = self.client.post(
            reverse('register'),
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_api_password_field_may_not_be_blank(self):
        """Test password field may not be blank"""
        data = {
            'email': 'teiker@libertymail.com',
            'username': 'way2teiker',
            'password': ''}

        response = self.client.post(
            reverse('register'),
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)
