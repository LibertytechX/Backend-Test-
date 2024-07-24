from django.contrib import admin
from User_App.models import CustomUser, Group
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Group)
