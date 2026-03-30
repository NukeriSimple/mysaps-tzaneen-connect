from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_staff', 'is_active', 'preferred_language')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'id_number', 'preferred_language', 
                                        'notification_method', 'large_font', 'voice_input')}),
        ('Address', {'fields': ('street_address', 'suburb', 'city', 'province', 'postal_code')}),
        ('Business', {'fields': ('is_business_owner', 'business_name', 'business_address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)