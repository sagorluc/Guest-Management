# myapp/socialaccount_adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.is_active = True  # Set user as active
        user.save()
        return user
    
    
    def pre_login(self,request,user,*,email_verification,signal_kwargs,email,signup,redirect_url):
        if not user.is_active:
            return self.respond_user_inactive(request, user)


    def respond_user_inactive(self, request, user):
        return HttpResponseRedirect(reverse("account_inactive"))
