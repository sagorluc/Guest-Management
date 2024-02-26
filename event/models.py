from django.db import models
# from django.contrib.auth.models import User
from API_authentication.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# User = settings.AUTH_USER_MODEL

# ============================ CREATE EVENT MODEL ==================================== 
class CollectAllGuestMail(models.Model):
    regis_guest_email = models.EmailField(max_length=200, default=False)
    event_id          = models.IntegerField(null=True)
  
class CreateEvent(models.Model):
    eventUser        = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user')
    eventOwnerName   = models.CharField(max_length= 25, blank=False, unique=True)
    eventTitle       = models.CharField(max_length= 200, blank=False)
    eventDate        = models.DateField(blank= False)
    eventTime        = models.TimeField(blank= False)
    totalSeat        = models.IntegerField(blank= False)
    eventLocation    = models.CharField(max_length= 250, blank= False)
    eventDescription = models.TextField(blank= False)
    token_numbers    = models.ManyToManyField('MultipleToken', related_name='tokens')
    # multiple_email   = models.ForeignKey(CollectAllGuestMail, on_delete=models.CASCADE, related_name='emails', null=True)
    token_verified   = models.BooleanField(default=False)
    eventCreatedDate = models.DateTimeField(auto_now_add= True, null=True)
    eventModifyDate  = models.DateTimeField(auto_now= True)
    
    class Meta:
        verbose_name = 'Create Event'
        verbose_name_plural = 'Create Events'
        ordering = ['id']
    
    def __str__(self) -> str:
        return str(self.eventUser)
    
       
# ============================ GENERATE TOKENS FOR EVENT GUEST ===========================   
class MultipleToken(models.Model):
    number      = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Multiple token'
        verbose_name_plural = 'All tokens'
        
           
# =============================== EVENT REGISTRATION MODEL ===============================   
class EventRegistration(models.Model):
    userE       = models.ForeignKey(User, on_delete=models.CASCADE, default=False, related_name='registration')
    event       = models.ForeignKey(CreateEvent, on_delete=models.CASCADE, blank=True, related_name='event')
    firstName   = models.CharField(max_length=25, blank=False)
    lastName    = models.CharField(max_length= 25, blank=False)
    email       = models.EmailField(max_length= 50, blank=False)
    friendName  = models.CharField(max_length=50, blank=True)
    friendEmail = models.EmailField(max_length=100, blank=True)
    phoneNumber = models.CharField(max_length=14, blank=False)
    totalPerson = models.IntegerField(blank=False)
    token_num   = models.CharField(max_length=21, unique=True, null=False)
    # all_email   = models.ManyToManyField('CollectAllGuestMail', blank=True)
    createDate  = models.DateTimeField(auto_now_add= True, null=True)
    modifyDate  = models.DateTimeField(auto_now= True)
    
    class Meta:
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'
        ordering = ['id']
    
       
    def __str__(self) -> str:
        return str(self.event)
    
       
class UpdateEvent(models.Model):
    eventOwnerName   = models.CharField(max_length=150)
    eventTitle       = models.CharField(max_length=150)
    eventDate        = models.DateField(blank=True)
    eventTime        = models.TimeField(blank=True)
    eventLocation    = models.CharField(max_length=300)
    eventDescription = models.TextField()
    