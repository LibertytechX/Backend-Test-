"""Manage admin page for main app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import *

# Register your models here.
# @admin.register(User)
# class UserAdmin(UserAdmin):
#     ordering = ('email',)
#     list_display = ('name',)
#     fieldsets = (
#         (None, {'fields': ('id',)}),
#         (
#             ('Personal info'),
#             {
#                 'fields': (
#                     'first_name',
#                     'last_name',
#                     'name',
#                     'email',
#                     'username',
#                     'password',
#                 )
#             },
#         ),
#         (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
#         (('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)