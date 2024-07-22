from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from faker import Faker


class UserTestsSetUp(APITestCase):

    def setUp(self):
        """ Handles set up of test variables and env for User. """
        self.faker = Faker()
        self.user_data = {
            'email': self.faker.email(),
            'password': self.faker.password(),
            'name': self.faker.name_female(),
        }
        self.user = get_user_model().objects.create_user(
            email=self.user_data['email'], password=self.user_data['password'])

        self.register_url = reverse('users-register')
        self.login_url = reverse('users-login')

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
