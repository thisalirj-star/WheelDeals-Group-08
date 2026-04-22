from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'company_name', 'is_active')
    list_filter = ('user_type', 'is_active')
    # Adds our custom fields to the admin edit page
    fieldsets = UserAdmin.fieldsets + (
        ('WheelDeals Info', {
            'fields': ('user_type', 'company_name', 'phone', 'address', 'profile_picture')
        }),
    )