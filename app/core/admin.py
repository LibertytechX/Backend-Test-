"""Manage admin page for main app."""
from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from  .models import Coin, Favourite
# from django.contrib import admin
User = get_user_model()


class UserAdmin(BaseUserAdmin):

    list_display = ('email', 'full_name', 'admin', 'active', 'staff',)
    list_filter = ('admin', 'active', 'staff')
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        # ('FULL NAME', {'fields': ('full_name',)}),
        ('permissions', {'fields': ('admin', 'active', 'staff')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class FavouriteAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'favourite'

    ]
    list_display_links = [
        'user',
    ]

    list_filter = [
        'user',
    ]

    search_fields = [
        'user__email',

    ]

    def favourite(self, obj):
        return "\n".join([a.name for a in obj.coin.all()])


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Coin)
admin.site.register(Favourite, FavouriteAdmin)