from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from product.models import Cart, Cartitems, Category, Order, Product
from model_bakery import baker

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = api_client.post('/store/products/', product, format="json", **header)
        return response
    return do_create_product

@pytest.fixture
def put_product(api_client : APIClient):
    def do_put_product(product):
        category = (baker.make(Category))
        category_id = category.__dict__.get('id')
        made_product = baker.make(Product, category=category, in_stock=10)
        id = made_product.__dict__.get('id')
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = api_client.put(f'/store/products/{id}/', product, format="json", **header)
        return response
    return do_put_product

@pytest.fixture
def patch_product(api_client : APIClient):
    def do_patch_product(product):
        category = (baker.make(Category))
        made_product = baker.make(Product, category=category, in_stock=10)
        id = made_product.__dict__.get('id')
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = api_client.put(f'/store/products/{id}/', product, format="json", **header)
        return response
    return do_patch_product

@pytest.fixture
def get_cart(api_client: APIClient):
    def do_get_cart():
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = api_client.get('/store/cart/', format="json", **header)
        return response
    return do_get_cart    

@pytest.fixture
def get_order(api_client: APIClient):
    def do_get_order():
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = api_client.get('/store/order', format="json", **header)
        return response
    return do_get_order    

@pytest.fixture
def update_cartitem(api_client: APIClient):
    def do_update_cartitem(request, cartitems=None, another_user=None):
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        user = baker.make(User)
        category = baker.make(Category)
        product = baker.make(Product, category=category)
        cart = baker.make(Cart, owner=user)
        cart = baker.make(Cartitems, cart=cart, product=product, quantity=10)
        cart_id = cart.id
        if another_user is None:
            api_client.force_authenticate(user=user)
        else:
            api_client.force_authenticate(user={})
        
        if cartitems is None:  
            cartitems = {
                    "requestType":"inbound",
                    "data": {
                        "product": 1,
                        "quantity": 10
                    }
                }
        else:
            cartitems = cartitems
        
        if request == 'patch':
            response = api_client.put(f'/store/cart/{cart_id}/', cartitems, format="json", **header)
        elif request == 'put':
            response = api_client.patch(f'/store/cart/{cart_id}/', cartitems, format="json", **header)

        return response
    return do_update_cartitem    


@pytest.mark.django_db
class TestCreateProduct(): 
        
    def test_403_if_user_is_not_staff(self, api_client, create_product):
        api_client.force_authenticate(user=User())
        category = baker.make(Category)
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product 10",
                    "price": 3000,
                    "description": "This is product 10",
                    "in_stock": 10,
                    "colors": ["red", "yellow", "pink"],
                    "category": category.id
                }
            }
        response = create_product(product)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_201_if_okay(self, api_client, create_product):
        category = baker.make(Category)
        category = category.__dict__
        category_id = category.get('id', None)
        api_client.force_authenticate(user=User(is_staff=True))
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product 10",
                    "price": 3000,
                    "description": "This is product 10",
                    "in_stock": 10,
                    "colors": ["red", "yellow", "pink"],
                    "category": category_id
                }
            }
    
        response = create_product(product)

        assert response.status_code == status.HTTP_201_CREATED
        
    def test_400_if_bad_data(self, api_client, create_product):
        api_client.force_authenticate(user=User(is_staff=True))
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product 10",
                    "price": 3000,
                    "description": "This is product 10",
                    "in_stock": 10,
                    "colors": ["red", "yellow", "pink"],
                    "category": "a"
                }
            }
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}

        response = create_product(product)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
@pytest.mark.django_db       
class TestGetProduct():
    def test_200_if_okay(self):
        client = APIClient()
        response = client.get('/store/products/')
        
        assert response.status_code == status.HTTP_200_OK
        
    def test_getSingle_200_if_okay(self):
        client = APIClient()
        category = (baker.make(Category))
        product = baker.make(Product, category=category, in_stock=10)
        id = product.__dict__.get('id')
        response = client.get(f'/store/products/{id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['in_stock'] == 10
        
@pytest.mark.django_db
class TestUpdateProduct():
    def test_200_if_put_is_okay(self, api_client, put_product):
        api_client.force_authenticate(user=User(is_staff=True))
        category = (baker.make(Category))
        category_id = category.__dict__.get('id')
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product updated",
                    "price": 3000,
                    "description": "This is product 10 ",
                    "in_stock": 10,
                    "colors": ["red", "yellow", "pink"],
                    "category": category_id
                }
            }
        
        response = put_product(product)
        assert response.status_code == status.HTTP_200_OK
             
    def test_200_if_patch_is_okay(self, api_client, patch_product):

        api_client.force_authenticate(user=User(is_staff=True))
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product 10",
                    "price": 3000,
                    "description": "This is product 10",
                    "colors": ["red", "yellow", "pink"]
                }
            }
        
        response = patch_product(product)

        assert response.status_code == status.HTTP_200_OK
        
    def test_400_if_put_with_bad_data(self, api_client, put_product):
        api_client.force_authenticate(user=User(is_staff=True))
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product 10",
                    "price": 3000,
                    "description": "This is product 10"
                }
            }
        
        response = put_product(product)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_400_if_patch_with_bad_data(self, api_client, patch_product):

        api_client.force_authenticate(user=User(is_staff=True))
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product 10",
                    "price": "3000",
                    "description": "This is product 10",
                    "in_stock": "10",
                    "in_colors": ["red", "yellow", "pink"],
                }
            }
        
        response = patch_product(product)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_401_if_put_as_anonymous_user(self, put_product):

        category = (baker.make(Category))
        category_id = category.__dict__.get('id')
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product updated",
                    "price": 3000,
                    "description": "This is product 10 ",
                    "in_stock": 10,
                    "colors": ["red", "yellow", "pink"],
                    "category": category_id
                }
            }
        
        response = put_product(product)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_401_if_patch_as_anonymous_user(self, patch_product):
        product = {
                "requestType":"inbound",
                "data": {
                    "name": "Product 10",
                    "price": 3000,
                    "description": "This is product 10",
                    "in_stock": 10,
                    "colors": ["red", "yellow", "pink"],
                }
            }
        
        response = patch_product(product)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

@pytest.mark.django_db
class TestGetCart():
    def test_200_if_okay(self, api_client, get_cart):
        user = baker.make(User)
        cart = baker.make(Cart, owner=user)
        api_client.force_authenticate(user=user)
        response = get_cart()
        
        assert response.status_code == status.HTTP_200_OK
        
    def test_401_if_anonymous(self, get_cart, api_client):
        response = get_cart()
        api_client.force_authenticate(user={})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db      
class TestGetOrder():
    def test_200_if_okay(self, api_client):
        client = APIClient()
        user = baker.make(User)
        order = baker.make(Order, owner=user)
        client.force_authenticate(user=user)
        response = client.get('/store/order/')

        assert response.status_code == status.HTTP_200_OK
        
    def test_401_if_anonymous(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.get('/store/order/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_200_forGetSingle_if_okay(self):
        client = APIClient()
        user = baker.make(User)
        order = baker.make(Order, owner=user)
        client.force_authenticate(user=user)
        
        order_id = order.__dict__.get('id')
        response = client.get(f'/store/order/{order_id}/')
        
        assert response.status_code == status.HTTP_200_OK

    def test_403_forGetSingle_if_anonymous(self):
        client = APIClient()
        user = baker.make(User)
        order = baker.make(Order, owner=user)
        client.force_authenticate(user={})
        
        order_id = order.__dict__.get('id')
        response = client.get(f'/store/order/{order_id}/')
        
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestCreateOrder():

    def test_403_if_user_is_anonymous(self):
        client = APIClient()
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = client.post('/store/order/', **header)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_200_if_okay(self):
        client = APIClient()
        client.force_authenticate(user=User())
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = client.post('/store/order/', data={"requestType": "inbound", "data":{"command": "checkout"}}, format="json", **header)
        
        
        assert response.status_code == status.HTTP_200_OK

    def test_400_if_bad_data(self):
        client = APIClient()
        client.force_authenticate(user=User())
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = client.post('/store/order/', data={"requestType": "inbound", "data":{"command": "baddata"}}, format="json", **header)
        
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestAddToCart():
    
    def test_403_if_user_is_anonymous(self):
        client = APIClient()
        category = (baker.make(Category))
        made_product = baker.make(Product, category=category, in_stock=10)
        id = made_product.__dict__.get('id')
        
        data = {
                "requestType": "inbound",
                "data": {
                    "product": id,
                    "quantity": 10
                    }
                }
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = client.post('/store/cart/', data=data, format="json", **header)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_201_if_okay(self, api_client, create_product):
        client = APIClient()
        client.force_authenticate(user=User())
        
        category = (baker.make(Category))
        made_product = baker.make(Product, category=category, in_stock=10)
        id = made_product.__dict__.get('id')
        
        data ={
                "requestType": "inbound",
                "data": {
                    "product": id,
                    "quantity": 10
                }
            }
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        response = client.post('/store/cart/', data=data, format="json", **header)
        
        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db    
class TestUpdateCartItem():
    def test_200_if_put_is_okay(self, update_cartitem):
        
        response = update_cartitem('put', cartitems=None, another_user=None)
        
        assert response.status_code == status.HTTP_200_OK
        
    def test_200_if_patch_is_okay(self, update_cartitem):
       
        response = update_cartitem('patch', cartitems=None, another_user=None)
        
        assert response.status_code == status.HTTP_200_OK
        
        
    def test_400_if_put_with_bad_data(self, update_cartitem):
        cartitems = {
                    "requestType":"inbound",
                    "data": {
                    }
                }
        response = update_cartitem('put', cartitems=cartitems, another_user=None)
       
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_400_if_patch_with_bad_data(self, update_cartitem):
        
        cartitems = {
                    "requestType":"inbound",
                    "data": {
                        "quantity_BAD": 10
                    }
                }
      
        response = update_cartitem('patch', cartitems=cartitems, another_user=None)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_401_if_put_as_anonymous_user(self, update_cartitem):
        
        response = update_cartitem('put', cartitems=None, another_user={})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_401_if_patch_as_anonymous_user(self, update_cartitem):
        
        response = update_cartitem('patch', cartitems=None, another_user={})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        


@pytest.mark.django_db
class TestVerifyOrder():

    def test_403_if_user_is_anonymous(self):
        client = APIClient()
        order = baker.make(Order)
        response = client.get(f'/store/verify-order/{order.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_200_if_okay(self,):
        client = APIClient()
        order = baker.make(Order)
        client.force_authenticate(user=User())
        response = client.get(f'/store/verify-order/{order.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['is_verified'] == True