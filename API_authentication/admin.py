from django.contrib import admin
from API_authentication.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_verified', 'verification_otp']
    
admin.site.register(User, UserAdmin)