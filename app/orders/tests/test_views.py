from django.urls import reverse
from rest_framework import status
from .test_setup import OrderTestsSetUp


class OrderTestViews(OrderTestsSetUp):
    """ Test suite for testing Order views. """

    def test_unauthenticated_user_cannot_place_order(self):
        """ Ensure unauthenticated user cannot place an order. """
        order_data = {
            'products': [
                {
                    'product': self.product_one.id,
                    'quantity': 1
                },
            ]
        }
        response = self.client.post(self.order_list_url,
                                    order_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_place_order(self):
        """ Ensure authenticated users can place an order with a product. """
        order_data = {
            'products': [
                {
                    'product': self.product_one.id,
                    'quantity': 1
                },
            ]
        }
        response = self.client.post(
            self.order_list_url,
            order_data,
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.get('products')), 1)

    def test_authenticated_user_can_place_order_of_multiple_products(self):
        """ Ensure authenticated users can place an order of multiple products. """
        order_data = {
            'products': [
                {
                    'product': self.product_one.id,
                    'quantity': 1
                },
                {
                    'product': self.product_two.id,
                    'quantity': 12
                },
            ]
        }
        response = self.client.post(
            self.order_list_url,
            order_data,
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.get('products')), 2)

    def test_authenticated_user_can_view_order_history(self):
        """ Ensure authenticated user can retrieve personalised order history. """
        # Create an order (do it this way to eliminate reliance on other tests)
        order_data = {
            'products': [
                {
                    'product': self.product_one.id,
                    'quantity': 1
                },
                {
                    'product': self.product_two.id,
                    'quantity': 12
                },
            ]
        }
        self.client.post(self.order_list_url,
                         order_data,
                         format='json',
                         headers={'Authorization': f"Bearer {self.token}"})

        # Retrieve order history
        response = self.client.get(
            reverse('orders-history'),
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('user')['email'], self.email)
        self.assertEqual(len(response.data[0].get('products')), 2)
