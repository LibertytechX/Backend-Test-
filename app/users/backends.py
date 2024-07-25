from typing import Any
from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import *

""" custom backend to authenticate using email"""


UserModel = get_user_model()

class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)

        if email is None or password is None:
            return
        
        try:
        
            user = UserModel.objects.get(
                email=email
            )
        except UserModel.DoesNotExist:
            raise ValidationError({"error":"invalid credentials"})
        
        except Exception as e:
            raise ValidationError({"error":"invalid credentials"})
           

        if user.check_password(password):
            print(user)
            return user
        return None