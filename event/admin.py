from django.contrib import admin
from event.models import (
    CreateEvent, 
    EventRegistration, 
    MultipleToken,
    CollectAllGuestMail,
    UpdateEvent,
)
from django.utils.translation import gettext_lazy as _
# Register your models here.

# ============================ EVENT ADMIN ====================================
class CreateEventAdmin(admin.ModelAdmin):
    list_display = [
        'id','eventUser', 
        'eventOwnerName', 'eventTitle', 
        'eventDate', 'eventTime', 
        'totalSeat', 'token_verified',
        ]
    ordering = ['id']
    


# ======================= EVENT REGISTRATION ADMIN ==============================       
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'userE', 
        'event', 'firstName', 
        'email', 'phoneNumber', 
        'totalPerson'
        ]
    ordering = ['id']
    
    class Meta:
        verbose_name = 'EventRegistration'
        verbose_name_plural = 'EventRegistrations'
        
# ======================= EVENT REGISTRATION ADMIN ==============================       
# class EventTokenNumberAdmin(admin.ModelAdmin):
#     list_display = ['id', 'event']
#     ordering = ['id']
    
# ======================= EVENT REGISTRATION ADMIN ==============================       
class EventMultipleTokenNumberAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'is_verified']
    ordering = ['id']
    
# ======================= EVENT REGISTRATION ADMIN ==============================       
class CollectAllGuestMailAdmin(admin.ModelAdmin):
    list_display = ['id', 'regis_guest_email', 'event_id']
    ordering = ['id']
    
# ======================= EVENT REGISTRATION ADMIN ==============================       
class UpdateEventAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'eventOwnerName', 
        'eventTitle', 'eventDate',
        'eventTime', 'eventLocation',
        'eventDescription',
    ]
    ordering = ['-id']
    
        
admin.site.register(CollectAllGuestMail, CollectAllGuestMailAdmin)
admin.site.register(UpdateEvent, UpdateEventAdmin)      
admin.site.register(CreateEvent, CreateEventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
# admin.site.register(TokenNumber, EventTokenNumberAdmin)
admin.site.register(MultipleToken, EventMultipleTokenNumberAdmin)