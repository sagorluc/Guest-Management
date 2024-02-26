from django.db import models
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from API_authentication.models import User
from django.conf import settings

# User = settings.AUTH_USER_MODEL

class EmailVerification(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_email")
    email_token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    
class GeneratePasswordToken(models.Model):
     user_pass             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_pass')
     forget_password_token = models.CharField(max_length= 200)
     created_at            = models.DateTimeField(auto_now_add=True)
     
     def __str__(self) -> str:
          return self.user_pass.username