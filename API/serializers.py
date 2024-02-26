from rest_framework import serializers
from event.models import CreateEvent, EventRegistration
from django.utils import timezone

# ========================== CREATE EVENT SERIALIZER ==============================
class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreateEvent
        fields = ['eventOwnerName', 'eventTitle', 'eventDate', 'eventTime', 'totalSeat', 'eventLocation', 'eventDescription']
        
    def validate(self, data):
        input_date = data.get('eventDate')
        input_time = data.get('eventTime')
        current_date = timezone.now().date()
        current_time = timezone.localtime(timezone.now()).time()

        if input_date and input_date < current_date:
            raise serializers.ValidationError('Invalid Date! Date must be in the future')

        if input_time:
            if not (9 <= input_time.hour <= 17):
                raise serializers.ValidationError('Event must be between 9am and 5pm')
            elif input_date == current_date and input_time <= current_time:
                raise serializers.ValidationError('Invalid Time! Time must be in the future')

        return data
    
    def validate_totalSeat(self, value):
        if value > 50:
            raise serializers.ValidationError("Total seat cannot be more than 50.")
        return value
    

    
# ======================== EVENT REGISTRATION SERIALIZER ============================
class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['firstName', 'lastName', 'email', 'phoneNumber', 'totalPerson']
        
    def validate_totalPerson(self, value):
        if value > 2:
            raise serializers.ValidationError('The number of persons should not be more than 2.')
        return value
