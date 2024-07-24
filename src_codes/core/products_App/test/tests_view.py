from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountTests(APITestCase):

    def setUp(self):
        self.product_url = reverse('login')
        self.user_data = {
            
        }
        