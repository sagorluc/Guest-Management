from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash, get_user_model
# from django.contrib.auth.models import User
from API_authentication.models import User
from authentication.forms import (
    RegistrationFrom, LoginForm, 
    CustomPasswordChangeForm, 
    CustomPasswordResetForm,
    LoginForm,
)
from authentication.models import (
    EmailVerification, 
    GeneratePasswordToken,
)
from authentication.email_setup import (
    activateEmail, 
    send_forget_password_mail,
)
from authentication.tokens import account_activation_token
import uuid
from django.dispatch import receiver
# from allauth.account.signals import user_logged_in

# @receiver(user_logged_in)
# def set_user_active(sender, request, user, **kwargs):
#     # Check if the user logged in via social account
#     if user.socialaccount_set.exists():
#         user.is_active = True
#         user.save()


# ========================= USER ACTIVATION ACCOUNT ===========================
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        
        messages.success(request, "Thank you for your email confirmation. You have done your registration successfully. Now you are good to go")
        return redirect('login')
    else:
        messages.error(request, "Activation link invalid!")
        
    return redirect('login')    


# ======================== CHANGE/UPDATE/RESET PASSWORD ======================
def send_email_for_forget_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "This email is not associated with any account.")
                return redirect('forget_password')
            
            send_forget_password_mail(request, user)
            messages.success(request, "An email with instructions to reset your password has been sent to your email.")
            return redirect('forget_password')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'registration/01password_reset_form.html', {'form': form})
     

# ============================= USER REGISTRATION ==============================
def user_register(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_verified = False
            user.save()
            
            email = form.cleaned_data.get("email")
            activateEmail(request, user, email)
            return redirect('login')
    else:
        form = RegistrationFrom()
    return render(request, 'register.html', {'form': form})


# ============================= USER LOGIN ======================================
def log_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email') 
            # username = request.POST.get('username') 
            password = request.POST.get('password')
            
            # is_exists = User.objects.filter(email=email).first()
            is_exists = User.objects.filter(email=email).first()
            if not is_exists or not is_exists.check_password(password):
                messages.error(request, "Invalid email or password") 
                return redirect('login')
                          
            user = authenticate(email=email, password = password)
            # print(user, '#################')
            if user is not None:
                login(request, user)
                messages.success(request, 'Loged in successfully')
                return redirect('home')
            else:
                messages.error(request, 'User not found')
                return redirect('login')  
        else:
            form = LoginForm()           
    return render(request, 'login.html', {'form': form})


# ============================= USER LOGOUT =================================
@login_required
def log_out(request):
        
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully.')
    return redirect('login')



