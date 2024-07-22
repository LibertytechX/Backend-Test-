from rest_framework import status
from .test_setup import UserTestsSetUp


class UserTestViews(UserTestsSetUp):

    def test_user_cannot_register_without_data(self):
        """
        Ensure users cannot register without providing data.
        """
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_with_duplicate_data(self):
        """
        Ensure users cannot register an existing email.
        """
        response = self.client.post(self.register_url,
                                    self.user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_with_correct_data(self):
        """
        Ensure users can register with correct data.
        """
        response = self.client.post(self.register_url, {
            'email': self.faker.email(),
            'password': self.faker.password(),
            'name': self.faker.name_male(),
        },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_login_successfully_and_get_tokens(self):
        """
        Ensure users can login and receive an access token and refresh token in response.
        """
        response = self.client.post(self.login_url,
                                    self.user_data,
                                    format='json')
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_cannot_login_with_incorrect_data(self):
        """
        Ensure users cannot login with incorrect credentials.
        """
        response = self.client.post(self.login_url, {
            'email': 'incorrect@mail.com',
            'password': 'somepassword'
        },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user_cannot_login(self):
        """
        Ensure inactive accounts cannot login.
        """
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url,
                                    self.user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'Inactive account')
