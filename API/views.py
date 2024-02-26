from django.shortcuts import render, get_object_or_404
from API.serializers import CreateEventSerializer, EventRegistrationSerializer
from event.models import CreateEvent, EventRegistration
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import serializers

# Create your views here.

#================================ EVENT CREATE RAED  ===============================
class EventListCreate(ListCreateAPIView):
    serializer_class = CreateEventSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
       user = CreateEvent.objects.filter(eventUser= self.request.user)
       # print(user, '#####################')
       return user

    def perform_create(self, serializer):
        serializer.save(eventUser=self.request.user)
        
        
#========================== EVENT READ UPDATE DELETE ==============================
class EventRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = CreateEventSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
       return CreateEvent.objects.filter(eventUser= self.request.user)
   
    def perform_update(self, serializer):
        return serializer.save(eventUser= self.request.user)
    

#================================ GUEST CREATE  ====================================
class GuestListCreate(ListCreateAPIView):
    serializer_class = EventRegistrationSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EventRegistration.objects.filter(userE= self.request.user)
    
    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id') # catch the event id
        print("line 44", event_id)
        
        if not event_id:
            raise serializers.ValidationError('There is no event id.')

        event = get_object_or_404(CreateEvent, id=event_id)
        serializer.save(userE=self.request.user, event=event)

    
#======================= GUEST READ UPDATE DELETE ===================================
class GuestRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = EventRegistrationSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.filter(userE=self.request.user)

    def perform_update(self, serializer):
        serializer.save(userE=self.request.user)



