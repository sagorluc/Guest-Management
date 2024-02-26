from django.urls import path
from API.views import EventListCreate, EventRetrieveUpdateDestroy,GuestListCreate, \
   GuestRetrieveUpdateDestroy

urlpatterns = [
    path('event_lc/', EventListCreate.as_view(), name="event_read_create"),
    path('event_rud/<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name="event_rud"),
    path('guest_lc/<int:event_id>/', GuestListCreate.as_view(), name="guest_read_create"),
    path('guest_rud/<int:pk>/', GuestRetrieveUpdateDestroy.as_view(), name="guest_rud"),
    
]
