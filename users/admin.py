from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'phone_number', 'first_name', 'last_name', 'is_staff', 'is_active']
    search_fields = ['email', 'phone_number', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('دسترسی‌ها'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('مجوزها'), {'fields': ('groups', 'user_permissions')}),
        (_('تاریخ‌های مهم'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
