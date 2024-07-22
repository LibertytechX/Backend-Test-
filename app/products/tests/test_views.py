from rest_framework import status
from .test_setup import ProductTestsSetUp


class ProductTestViews(ProductTestsSetUp):
    """Test suite to test Product CRUD operations based on the following assumptions:
    
        - User must be authenticated on all routes
        - User must be authorised to make write actions (PUT, DELETE, PATCH etc)
    """

    def test_user_cannot_create_product_without_authentication(self):
        """Ensure users cannot create product without authentication. """
        response = self.client.post(self.product_list_url,
                                    self.product_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_cannot_create_product_without_authorization(
            self):
        """Ensure unauthorised users cannot create product. """
        response = self.client.post(
            self.product_list_url,
            self.product_data,
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            'Staff level or higher is required to update records',
            response.data.get('detail'),
        )

    def test_user_can_create_product_with_authorization(self):
        """Ensure authorised users (ie., Staff or Higher) can successfully create a product. """
        self.user.is_staff = True  # make user a staff
        self.user.save()
        # Now try creating a product again
        self.product_data[
            'category'] = 'Electronics'  # Add category to product data (it should be an already created category)
        response = self.client.post(
            self.product_list_url,
            self.product_data,
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_view(self):
        """Ensure we can retrieve the correct list of products. """
        response = self.client.get(
            self.product_list_url,
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_detail_view(self):
        """Ensure we retrieve correct product by ID. """
        response = self.client.get(
            self.product_detail_url,
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.product_data['name'])

    def test_authorised_user_can_update_product(self):
        """Ensure authorised user can update product by ID. """
        self.user.is_staff = True  # make user a staff
        self.user.save()

        new_product_name = self.faker.name()
        response = self.client.patch(
            self.product_detail_url, {'name': new_product_name},
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), new_product_name)

    def test_authorised_user_can_delete_product(self):
        """Ensure authorised user can delete product by ID. """
        self.user.is_staff = True  # make user a staff
        self.user.save()

        response = self.client.delete(
            self.product_detail_url,
            format='json',
            headers={'Authorization': f"Bearer {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
