from rest_framework import permissions

import jwt

from app.settings import SECRET_KEY
from core.models import User

class IsJWTValidated(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):

        try:
            if not request.headers['Authorization']:
                raise Exception("No token")
            
            token = str(request.headers['Authorization']).split(' ')[1]
            payload = jwt.decode(str(token), SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id = payload['user_id'])
            request.user = user
            
            return True
        
        except:
            return False