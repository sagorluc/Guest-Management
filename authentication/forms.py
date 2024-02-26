from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from API_authentication.models import User
from django import forms
from django.contrib import messages
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

# ============================ USER REGISTRATION FORM ===============================
class RegistrationFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # chaeck the both passowrd is matched 
    def clean(self):
        cleaned_data     = super(RegistrationFrom, self).clean()
        password         = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    def __init__(self, *args, **kwargs):
        super(RegistrationFrom, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        
        # Remove help text
        for field_name in self.fields.keys():
            self.fields[field_name].help_text = ''
        

# ============================= USER LOGIN FORM =================================       
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    # username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    captcha = ReCaptchaField()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     password = cleaned_data.get('password')

    #     user = User.objects.filter(email=email).first()

    #     if not user or not user.check_password(password):
    #         messages.error("Invalid email or password" )

    #     return cleaned_data
    

class CustomPasswordChangeForm(forms.Form):
    new_password     = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    
    # set place holder by overriding    
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email account'