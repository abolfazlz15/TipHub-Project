from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import *
from .models import User, Teacher, OTPCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationFormm


    list_display = ('showImage', 'email', 'full_name', 'username', 'phone_number', 'is_admin', 'is_superuser')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('phone_number', 'full_name', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_display_links = ('showImage', 'email', 'full_name', 'username', 'phone_number')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'full_name', 'avatar', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()
    def get_form(self, request, obj=None, **kwargs):
        obj = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            obj.base_fields['is_superuser'].disabled = True
        return obj

admin.site.register(User, UserAdmin)

admin.site.register(Teacher)
admin.site.register(OTPCode)