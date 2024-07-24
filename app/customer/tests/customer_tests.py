from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from model_bakery import baker

@pytest.fixture
def create_user(api_client):
    def do_create_user(user:str):
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        
        if user == 'good':
            user = {
                "requestType": "inbound",
                "data":{
                    "username":"testuser",
                    "email":"testuser@gmail.com",
                    "password":"UserTest@123"
                }
            }
        else:
            user = {
                "requestType": "inbound",
                "data":{
                    "username":"testuser",
                }
            }
        response = api_client.post('/customer/user/', user, format="json", **header)
        return response
    return do_create_user


@pytest.fixture
def update_user(api_client : APIClient):
    def do_update_user(user:str, method:str, is_auth=False):
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}
        
        if user == 'good':
           user_detail =  {
            "requestType": "inbound",
            "data": {
                "first_name": "Test",
                "last_name": "Testing",
                "address": "Test user a",
                "phone": "08100000000",
                "state": "Oyo",
                "country": "Nigeria"
                }
            }
        else:
            user_detail =  {
            "requestType": "inbound",
            "data": {}
            }
        
        if is_auth:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            
        if method == 'put':
            
            response = api_client.put('/customer/user/', user_detail, format="json", **header)
        elif method == 'patch':
            response = api_client.patch('/customer/user/', user_detail, format="json", **header)
        
        return response
    return do_update_user

@pytest.fixture
def get_user(api_client : APIClient):
    def do_get_user(is_auth=False):
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}   
        if is_auth:
            user = baker.make(User)
            api_client.force_authenticate(user=user)
            
        response = api_client.get('/customer/user/', **header)
        
        return response
    return do_get_user

@pytest.fixture
def login_user(api_client : APIClient):
    def do_login_user(user:str):
        header = {'HTTP_X-Api-Key':'R7zoOlmyoHSWZH1NMU9RTzUv5nfSo944YGLHX6SXYlYxzll3rHISEAgbdj3aItmQdwf9Axo2d4BuLevRoKsJaISarl8dYPoA18eojUzgBlobCo3oHu2WkGEFVC2f1uAp'}   

        if user == 'good':
            loginuser = baker.make(User, username="testing", password="@checkpass")
            user_detail =  {
                "requestType": "inbound",
                "data": {
                    "username": "testing",
                    "password": "@checkpass"
                    }
                }
        else:
            user_detail =  {
                "requestType": "inbound",
                "data": {
                    "username": "unexisting",
                    "password": "unexisting"
                    }
                }
            
        
        response = api_client.post('/customer/login/', user_detail, format="json",**header)
        
        return response
    return do_login_user


@pytest.mark.django_db  
class TestLoginUser():
    def test_200_if_okay(self, login_user):
        response = login_user('good')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_400_if_anonymous(self, login_user):
        response = login_user('bad')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db  
class TestGetUserDetails():
    
    def test_200_if_okay(self, get_user):
        response = get_user(True)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_401_if_anonymous(self, get_user):
        response = get_user(False)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db  
class TestUpdateUserDetails():
    
    def test_200_if_put_okay(self, update_user):
        response = update_user(user="good", method="put", is_auth=True)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_200_if_patch_okay(self, update_user):
        response = update_user(user="good", method="patch", is_auth=True)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_401_if_put_anonymous(self, update_user):
        response = update_user(user="good", method="put", is_auth=False)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_401_if_patch_anonymous(self, update_user):
        response = update_user(user="good", method="patch", is_auth=False)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_400_if_put_bad_data(self, update_user):
        response = update_user(user="bad", method="put", is_auth=True)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_400_if_patch_bad_data(self, update_user):
        response = update_user(user="bad", method="patch", is_auth=True)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db  
class TestCreateUser():
    
    def test_200_if_okay(self, create_user):
        response = create_user('good')
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_400_if_bad_data(self, create_user):
        response = create_user("bad")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
