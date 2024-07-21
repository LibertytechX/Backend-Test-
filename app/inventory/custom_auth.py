from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model
User = get_user_model()#get the user model used for the entire project


'''
This class is responsible for user login
permiting them to use their names or email  to login
'''
class EmailNameAuthBackend(ModelBackend):
    def authenticate(self,requst,email =None, password = None):
        try:
            user = User.objects.get(email=email)
            success = user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(name=email)
                success = user.check_password(password)
                if success:
                    return user
            except User.DoesNotExist:
                    return None
