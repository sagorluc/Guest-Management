from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from authentication.tokens import account_activation_token
from API_authentication.models import User
# from django.contrib.auth.models import User
import random

# =============================== For Activation Account =================================
def activateEmail(request, user, to_email):
    mail_subject = "Activate your account"
    otp = random.randint(100000, 999999)
    message      = render_to_string("activate_account.html", {
        'user'     : user.username,
        'domain'   : get_current_site(request).domain,
        'uid'      : urlsafe_base64_encode(force_bytes(user.pk)),
        'token'    : account_activation_token.make_token(user),
        'protocol' : 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        user = User.objects.get(email=to_email) # save OTP to database
        user.verification_otp = otp
        user.save()
        mess = mark_safe(f"Hi <b>{user}</b>, go to your email <b>{to_email}</b>. We have send a link to activate your account. Note: if it's not found in inbox then check in the spam.")
        messages.success(request, mess)
    else:
        mess = mark_safe(f"Problem sending email to <b>{to_email}</b>")
        messages.error(request, mess)
        

# =========================== Change/Update/Reset Password ===============================
def send_forget_password_mail(request, user):
    current_site = get_current_site(request)
    subject = 'Reset Your Password'
    email_template_name = 'registration/05password_reset_email.html'
    context = {
        'user'  : user,
        'domain': current_site.domain,
        'uid'   : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    }
    message = render_to_string(email_template_name, context)
    to_email = user.email
    send_email(subject, message, to_email)

def send_email(subject, message, to_email):
    email = EmailMessage(subject, message, to=[to_email])
    email.send()      
        
# =========================== API REGISTRATION ACCOUNT MAIL ==============================       
def send_otp_via_email(email):
    subject = "Your OTP number for registration account"
    otp_number = random.randint(100000, 999999)
    message = f"Your OTP is: {otp_number}"
    from_email = settings.EMAIL_HOST
    send_mail(subject, message, from_email, [email])
    
    # Save otp into UserModel
    user_obj = User.objects.get(email=email)
    user_obj.verification_otp = otp_number
    user_obj.save()