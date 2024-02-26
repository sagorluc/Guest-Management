from django.urls import path
from API_authentication.views import (
    UserRegistrationView, 
    UserLoginView, 
    UserLogoutView, 
    UserView,
    UserVerifyAccountView,
)

urlpatterns = [
    path('registration_api/', UserRegistrationView.as_view(), name='register_api'),
    path('login_api/', UserLoginView.as_view(), name='login_api'),
    path('logout_api/', UserLogoutView.as_view(), name='logout_api'),
    path('user_api/', UserView.as_view(), name='user_api'),
    path('verify_account/', UserVerifyAccountView.as_view(), name='verify_api'),
]
