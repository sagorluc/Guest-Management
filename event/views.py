from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from event.forms import CreateEventForm, EventRegistrationForm, UpdateGuestForm
from event.models import (
    CreateEvent, 
    EventRegistration, 
    MultipleToken, 
    CollectAllGuestMail, 
    UpdateEvent,
)
from event.gen_token_for_event import generate_token, create_tokens_for_event
from event.event_email import send_token_email
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext_lazy
from event.event_email import send_email_to_guest, send_mail_to_all_event_guest
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from datetime import datetime
import ast
# Create your views here.

# ============================= SHOW ALL EVENT ==================================
@login_required
def all_event(request):
   all_events = CreateEvent.objects.all()
   
   event_data = []
   for event in all_events:
        guests = EventRegistration.objects.filter(event=event)
        total_person = sum(guest.totalPerson for guest in guests)
        available_seat = event.totalSeat - total_person

        event_data.append({
            'event': event,
            'available_seat': available_seat,
        })
   # print(event_data)

   context = {
        'all_datas': event_data,
        # 'all_events': all_events
        
    }

   return render(request, 'show_all_event.html', context)

# ============================= CREATE EVENT ==================================            
@login_required
def create_event(request):
    form = CreateEventForm()
    update_id = 200 + 1
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            total_seat = request.POST.get('totalSeat')
            event_user = form.save(commit=False)
            # event_user.id = update_id
            event_user.eventUser = request.user # eventUser is current user
            event_user.save()
            
            # create_event_instance = CreateEvent.objects.get(pk=event_user.pk)
            token = create_tokens_for_event( event_user, int(total_seat)) # generate token
            to_email = request.user.email                 
            # Send the token to the current user via email
            send_token_email(event_user, to_email, total_seat, token)
            messages.success(request, "We have send the token number for your guest in you email")
            return redirect('home')
    else:
        form = CreateEventForm()
    return render(request, 'create_event.html', {'forms': form})

# ============================= EVENT REGISTRATION ==============================
@login_required
def event_registration(request, id):
    event = CreateEvent.objects.get(pk=id) # instance of event
    user = request.user
    update_id = 100 + 1
    # not allow to registration more then one event
    is_registered = EventRegistration.objects.filter(userE=request.user, event=event).first()
    if is_registered:
        return render(request, 'error_page.html', {'event': event})
   
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            input_seat         = form.cleaned_data['totalPerson']
            input_token        = form.cleaned_data['token_num']
            input_email        = form.cleaned_data['email']
            input_friend_name  = request.POST.get('friendName')
            input_friend_email = request.POST.get('friendEmail')
            input_tokens       = [token.strip() for token in input_token.split(',')]
            
            email_list = []
            email_list.append(input_email)
            email_list.append(input_friend_email)
                                  
            # check if the user put more then the available seat 
            guests       = EventRegistration.objects.filter(event= event)  
            total_person = sum(guest.totalPerson for guest in guests)   
            total_seat   = event.totalSeat           
            if total_person <= total_seat:
                available_seat = total_seat - total_person               
                if input_seat > available_seat:
                    return render(request, 'not_seat_available.html')
                
            # Check if the user token is valid
            tokens = event.token_numbers.all()
            if input_seat != len(input_tokens):
                messages.error(request, "Person with the token does not match")
                return redirect('event_register', event.id)
            
            for input_token in input_tokens:
                token_matched = False
                for token in tokens:
                    if input_token.strip() == token.number:
                        token_matched = True
                        if token.is_verified:
                            messages.error(request, f"The token '{input_token}' has already been used.")
                            return redirect('event_register', event.id)
                        else:
                            token.is_verified = True
                            token.save()
                            break  # Exit the loop once the token is marked as used
                        
                if not token_matched:
                    messages.error(request, f"The token '{input_token}' is not valid.")
                    return redirect('event_register', event.id)

            for email in email_list:
                CollectAllGuestMail.objects.create(regis_guest_email=email, event_id=event.id)
                                            
            registration             = form.save(commit=False) # not saveing immediately bcz of want to to manipulate the data
            # registration.id          = update_id
            registration.friendName  = input_friend_name
            registration.friendEmail = input_friend_email
            registration.userE       = user  # current user put in the event registration user
            registration.event       = event # event put under event registration 
            registration.save()
            send_email_to_guest(
                registration.id, 
                registration.event, 
                email_list,
                               
                )
            messages.success(request, 'Registration successfull. You will get mail very soon')
            return redirect('dashboard')
    else:
        form = EventRegistrationForm()
    return render(request, 'event_registration.html', {'event': event, 'forms': form})


# ============================= EVENT DETAILS ==================================
@login_required
def event_details(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)
    guests = EventRegistration.objects.filter(event= event)
    
    total_person = sum(guest.totalPerson for guest in guests)   
    # print(total_person)
    total_seat = event.totalSeat
    # totalGuest = len(guest)

    if total_person <= total_seat:
        available_seat = total_seat - total_person
            
    context =  {
        
        'event': event, 
        'guests': guests,
        'available_seat' : available_seat,
        
        }
        
    return render(request, 'event_details.html', context)



# ============================= GUEST DETAILS ==================================
@login_required
def guest_details(request, id=None):
    guest = EventRegistration.objects.get(id= id)
    return render(request, 'guest_details.html', {'guest': guest})


# ============================= UPDATE DETAILS ==================================
@csrf_exempt
@login_required  
def update_event(request, id=None):
    event = get_object_or_404(CreateEvent, id=id) # instance of event
   
    if request.method == 'POST':
        form = CreateEventForm(request.POST, instance=event)
        if form.is_valid():
            input_date = form.cleaned_data['eventDate']
            input_time = form.cleaned_data['eventTime']
            current_date = timezone.now().date()
            current_time = timezone.localtime(timezone.now()).time()
            
            previous_event_data = CreateEvent.objects.filter(pk=event.pk).first()
            print(previous_event_data, '############## line 205')
                       
            if previous_event_data:
                change = track_changes_event(previous_event_data, event)
                if change:
                    # Current and previus value
                    eventDate_dict    = change.get('eventDate', {'previous_value': previous_event_data.eventDate, 'updated_value': previous_event_data.eventDate})
                    eventTime_dict    = change.get('eventTime', {'previous_value': previous_event_data.eventTime, 'updated_value': previous_event_data.eventTime}) 
                    event_owner_name  = change.get('eventOwnerName', previous_event_data.eventOwnerName)   
                    event_title       = change.get('eventTitle', previous_event_data.eventTitle)   
                    event_location    = change.get('eventLocation', previous_event_data.eventLocation) 
                    event_description = change.get('eventDescription', previous_event_data.eventDescription)  
                       
                    # Extract the date strings from the dictionary
                    eventDate_str = eventDate_dict.get('updated_value', previous_event_data.eventDate).isoformat()

                    # Extract the time string and convert it to ISO 8601 format
                    eventTime_str = eventTime_dict.get('updated_value', previous_event_data.eventTime).strftime('%H:%M:%S')

                    # Combine date and time strings
                    combined_datetime_str = f"{eventDate_str}T{eventTime_str}"

                    # Parse ISO 8601 formatted datetime string into a datetime object
                    combined_datetime = datetime.fromisoformat(combined_datetime_str)
                    date = combined_datetime.date()
                    time = combined_datetime.time()
                    
                    UpdateEvent.objects.create(
                        eventOwnerName=event_owner_name,
                        eventTitle=event_title,
                        eventDate=date,
                        eventTime=time,
                        eventLocation=event_location,
                        eventDescription=event_description
                    )
                    # print('insite update ##############')
                    # Get the CollectAllGuestMail instance associated with the event
                    to_email = []
                    distinct_email = set()
                    all_mail = CollectAllGuestMail.objects.filter(event_id=event.id)
                    for mail in all_mail:
                        email = mail.regis_guest_email
                        to_email.append(email)

                    # print(to_email, '############ line 242')
                    send_mail_to_all_event_guest(
                        event.id, event_owner_name, 
                        event_title, date, time, 
                        event_location, 
                        event_description, 
                        to_email,
                        )
                    messages.success(request, 'Information update successfully. It will inform to your all guest by email!!')
                    return redirect('event_details', event.id)
                else:
                    messages.success(request, 'Nothing updated')
                    return redirect('update_event', event.id)
                        
            else:
                if input_date and input_date < current_date:
                    messages.error(request, 'Invalid Date! Date must be in the future')
                elif input_time:               
                    if not (9 <= input_time.hour <= 17):
                        messages.error(request, 'Event must be between 9 am and 5 pm')
                    elif input_date == current_date and input_time <= current_time:
                        messages.error(request, 'Invalid Time! Time must be in the future')
                    else:
                        form.save()
                        messages.success(request, 'Event updated successfully')
                        return redirect('event_details', event.id)
                    
        # else:
        #     form.save()
        #     messages.success(request, 'Event updated successfully')
        #     return redirect('event_details', event.id)
    else:
        form = CreateEventForm(instance=event)

    return render(request, 'update_event.html', {'form': form, 'event': event})


def track_changes_event(previous_data, updated_data):
    changes = {}
    # Compare each field of the event model
    for field in ['eventOwnerName', 'eventTitle', 'eventDate', 'eventTime', 'eventLocation', 'eventDescription']:
        previous_value = getattr(previous_data, field)
        updated_value = getattr(updated_data, field)
        if previous_value != updated_value:
            changes[field] = {
                'previous_value': previous_value,
                'updated_value': updated_value
            }
    return changes

# ============================= UPDATE GUEST ==================================
@login_required
def update_guest(request, id=None):
    guest = get_object_or_404(EventRegistration, id=id)
    
    if request.method == 'POST':
        form = UpdateGuestForm(request.POST, instance = guest)
        if form.is_valid():
            input_person = form.cleaned_data['totalPerson']
            
            if input_person > 2:
               messages.error(request, 'Person should not be more the 2.')
               
            # Track if the data is changes
            guest_previus_data = EventRegistration.objects.filter(pk=guest.id).first()            
            is_changes = track_changes_guest(guest_previus_data, guest)
            
            if not is_changes:
                messages.success(request, 'Nothings updated')
                return redirect('update_guest', guest.id)
                   
            form.save()
            messages.success(request, 'Your infomation updated successfully.')
            return redirect('guest_details', guest.id)
    else:
        form = UpdateGuestForm(instance = guest)
    return render(request, 'update_guest.html', {'form': form}) 

def track_changes_guest(previous_data, updated_data):
    changes = {}
    # Compare each field of the event model
    for field in ['firstName', 'lastName', 'email', 'phoneNumber', 'totalPerson', 'friendName', 'friendEmail']:
        previous_value = getattr(previous_data, field)
        updated_value = getattr(updated_data, field)
        if previous_value != updated_value:
            changes[field] = {
                'previous_value': previous_value,
                'updated_value': updated_value
            }
    return changes             
                
# ============================= DELETE EVENT ==================================
@login_required
def delete_event(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)

    if request.user != event.eventUser:
        return HttpResponse('Unathorized user')

    if request.method == 'POST':
        event.delete()
        return redirect('dashboard')

    return render(request, 'delete_event.html', {'event': event})


# ============================= DELETE GUEST ==================================
@login_required
def delete_guest(request, id=None):
    guest_del = get_object_or_404(EventRegistration, id=id) # get the instance
    event_instance = guest_del.event
    token_numbers_queryset = event_instance.token_numbers.all()
    token_numbers_list = list(token_numbers_queryset.values_list('number', flat=True)) # make list

    guest_person = guest_del.totalPerson
    
    if request.method == 'POST':
        # Input data
        input_person = request.POST.get('person')
        input_token = request.POST.get('token')
        token_list = [token.strip() for token in input_token.split(',')]

        # Check queryset token and input qu:set person and token list and input person not match
        if len(token_list) != guest_person and len(token_list) != input_person:
            messages.error(request, 'Guest with token does not match.')
            return redirect('delete_guest', id=id)

        # take out all the token form input token
        for input_token in token_list:
            if input_token not in token_numbers_list:
                messages.error(request, f"The token '{input_token}' is not valid.")
                return redirect('delete_guest', id=id)

            token_instance = token_numbers_queryset.get(number=input_token)
            
            if not token_instance.is_verified:
                messages.error(request, f"The token '{input_token}' has already been deactivated.")
                return redirect('delete_guest', id=id)

            token_instance.is_verified = False
            token_instance.save()

        guest_del.delete()
        messages.success(request, f'{guest_del.userE.username} this guest has been deleted successfully!!')
        return redirect('dashboard')

    return render(request, 'delete_guest.html', {'guest': guest_del})
    

# ============================= DASHBOARD ==================================   
@login_required   
def dashboard(request):
    events = CreateEvent.objects.filter(eventUser= request.user)  
    guests = EventRegistration.objects.filter(userE= request.user)
     
    context = {
        'events' : events,
        'guests' : guests,
    }   
    return render(request, 'dashboard.html', context)


# ========================== SEARCH EVENT AND GUEST ===============================
@login_required
def search_guest_event(request):
    input_query = request.GET.get('keyword')
    
    events = CreateEvent.objects.all()
    guests = EventRegistration.objects.all()
    
    # number base searching
    try:
        id_query = int(input_query)
        events = events.filter(id=id_query)
    except ValueError:
        pass  
    
    
    events = events.filter(
        Q(eventTitle__icontains=input_query) |
        Q(eventUser__username__icontains=input_query) |
        Q(eventOwnerName__icontains=input_query) |
        Q(eventDate__icontains=input_query) |
        Q(eventLocation__icontains=input_query)
    )
    
    
    guests = guests.filter(
        Q(firstName__icontains=input_query) |
        Q(lastName__icontains=input_query) |
        Q(email__icontains=input_query)
    )
    
    # date-based filtering
    try:
        date_input = timezone.datetime.strptime(input_query, '%Y-%m-%d').date()
        events = events.filter(eventDate=date_input)
        guests = guests.filter(createDate=date_input)
    except ValueError:
        pass

    
    if events:
        context = {'events' : events, }
        return render(request, 'search_guest_event.html', context)
    else:
        context = {'guests' : guests}
        return render(request, 'search_guest_event.html', context)
    
    

# =========================== FILTER EVENT AND GUEST ===============================       
@login_required
def filter_event(request):
    input_event_date = request.GET.get('eventDate')
    input_event_location = request.GET.get('location')
    
    events = CreateEvent.objects.filter(eventUser= request.user)
    guests = EventRegistration.objects.filter(userE= request.user)
    
    if input_event_date:
        events = events.filter(Q(eventDate=input_event_date))
        guests = guests.filter(Q(event__eventDate=input_event_date))
        
    if input_event_location:
        events = events.filter(Q(eventLocation__icontains= input_event_location))
        guests = guests.filter(Q(event__eventLocation__icontains=input_event_location))
        
    return render(request, 'dashboard.html', {'events' : events, 'guests' : guests})


# =========================== COMMON DATA =============================
# def get_common_data(event, guests):
#     total_person = sum(guest.totalPerson for guest in guests)
#     total_seat = event.totalSeat

#     common_data = {
#         'event': event,
#         'guests': guests,
#     }

#     if total_person <= total_seat:
#         common_data['available_seat'] = total_seat - total_person

#     return common_data