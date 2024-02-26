from django.urls import path
from authentication.views import (
    user_register, log_in, log_out, 
    activate, send_email_for_forget_password
    )
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('forget-password/', send_email_for_forget_password, name='forget_password'),
    # path('change-password/<uidb64>/<token>', change_password, name='change_password'),
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/01password_reset_form.html"), name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/02password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/03password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/04password_reset_complete.html"), name='password_reset_complete'),
]
