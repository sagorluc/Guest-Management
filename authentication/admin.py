from django.contrib import admin
from authentication.models import EmailVerification, GeneratePasswordToken

class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_token', 'is_verified']
    ordering     = ['id']
    
class GeneratePasswordTokenAdmin(admin.ModelAdmin):
    list_display = ['user_pass', 'forget_password_token']
    ordering     = ['id']
    
admin.site.register(EmailVerification, EmailVerificationAdmin)
admin.site.register(GeneratePasswordToken, GeneratePasswordTokenAdmin)