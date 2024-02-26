from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from event.models import CreateEvent
from django.conf import settings

def send_token_email(event, to_email, total_seat, token):
    subject = 'Token for Your event guest'
    # Render the email message using a template
    html_message = render_to_string('token_email.html', 
                {
                'event_id': event.id, 
                'total_seat': total_seat, 
                'token': token
        })
    plain_message = strip_tags(html_message)  # Strip HTML tags for plain text version
    from_email = settings.EMAIL_HOST 
    to_email = to_email
    send_mail(subject, plain_message, from_email, [to_email], html_message= html_message)
    
    
def send_email_to_guest(register_id, register_event, recipent_mail_list):
    
    event_instance = CreateEvent.objects.get(pk=register_event.id)
    
    subject = "You are welcome to join event"
    html_message = render_to_string('send_mail_to_guest.html', {
        'register_id' : register_id,
        'event_id': event_instance.id,
        'event_title': event_instance.eventTitle,
        'event_date': event_instance.eventDate,
        'event_time': event_instance.eventTime,
        'event_location': event_instance.eventLocation,
        'event_description': event_instance.eventDescription,
       
    })
    
    plain_text = strip_tags(html_message)
    from_email = settings.EMAIL_HOST
    to_emails = recipent_mail_list
    for to_email in to_emails:
        send_mail(subject, plain_text, from_email, [to_email], html_message=html_message)
        
        
def send_mail_to_all_event_guest(event_id, event_owner_name, event_title, date, time, event_location, event_description, recipent_mail_list):
    subject = 'Updated some of infomation of your event'
    html_message = render_to_string('mail_update_data.html', {
        'event_id': event_id,
        'event_owner_name': event_owner_name['updated_value'],
        'event_title': event_title['updated_value'],
        'date': date,
        'time': time,
        'event_location': event_location['updated_value'],
        'event_description': event_description['updated_value'],
    })
    
    plain_text = strip_tags(html_message)
    from_email = settings.EMAIL_HOST
    to_emails = recipent_mail_list
    for to_email in to_emails:
        send_mail(subject, plain_text, from_email, [to_email], html_message= html_message)