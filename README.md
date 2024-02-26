# Event Registration System

This Django-based Event Management System allows users to create events, manage event details, and handle event registrations. The system consists of two main components: creating events and managing event registrations.

## Featurs

### Create Event Form

The CreateEventForm class in the forms.py file defines a form for creating events. It includes fields such as event owner name, title, date, time, total seats, location, and description. The form provides placeholders and validates the input data, ensuring that the date is in the future and the time falls within the acceptable range

### Event Registration Form

The EventRegistrationForm class handles the registration process for events. Users can register for an event by providing their first name, last name, email, phone number, and the number of attendees. The form includes placeholders and validates the number of attendees, restricting it to a maximum of 2.

### Views

* Show All Events (all_event): Displays all events, including details such as available seats.

* Create Event (create_event): Allows users to create new events. Validates input data and the maximum attendence allow 50 person and save the event details. 

* Event Registration (event_registration): Handles user registration for a specific event. Validates input data, checks available seats, and if the current user already registered one time then that user not able to access registration for second time in that event.also if the event already fillup with the full of attendence then the ragistration button would be disabled.

* Event Details (event_details): Displays details of a specific event, including registered guests and available seats.

* Guest Details (guest_details): Shows details of a registered guest.

* Update Event (update_event): Allows users to update event details. Validates input data and updates the event information.

* Update Guest (update_guest): Enables the update of guest registration details, such as the number of attendees.

* Delete Event (delete_event): Allows users to delete events they created.

* Delete Guest (delete_guest): Allows users to remove a guest's registration.

* Dashboard (dashboard): Provides an overview of events created by the user and their event registrations.

* Search Events and Guests (search_guest_event): Allows users to search for events or guests based on keywords, event titles, usernames, and more.

* Filter Events (filter_event): Enables users to filter events based on date and location.

### How to use

* Create Event: Navigate to the "Create Event" page, fill in the required details, and submit the form.

* Register for an Event: Visit the all event page and click registration button for the event by providing your information.

* View Event Details: Explore details of each event, including registered guests and available seats.

* Update Event: Modify event details by navigating to the dashboard page and click the "Update" button.

* Update Guest Registration: Change the number of attendees and firstname, lasname, email for a guest by selecting the "Update" button.

* Delete Event: Remove an event by selecting the "Delete" button on the dashboard page.

* Delete Guest Registration: Remove a guest's registration by selecting the "Delete" button.

* Dashboard: Access an overview of events created and guest registrations.

* Search and Filter: Utilize search and filter functionalities to find specific events or guests.

# Django Rest Framework API View
These Django Rest Framework views provide API endpoints for managing events and guest registrations.

### Features
#### Event List and Create (EventListCreate)
##### Endpoint: /api/event_lc/
##### Methods: GET, POST
###### Description:
* Retrieves a list of events created by the authenticated user.
* Allows the authenticated user to create a new event.
* Automatically associates the event with the current user.

### Event Retrieve, Update, and Delete (EventRetrieveUpdateDestroy)
##### Endpoint: /api/event_rud/<event_id>/
##### Methods: GET, PUT, PATCH, DELETE
###### Description:
* Retrieves details of a specific event created by the authenticated user.
* Allows the authenticated user to update or delete the event.
* Ensures that users can only access and modify events they created.

### Guest List and Create (GuestListCreate)
##### Endpoint: /api/guest_lc/<event_id>/
##### Methods: GET, POST
###### Description:
* Retrieves a list of guest registrations for a specific event created by the authenticated user.
* Allows the authenticated user to register guests for the specified event.
* Automatically associates the guest registration with the current user and the selected event.

### Guest Retrieve, Update, and Delete (GuestRetrieveUpdateDestroy)
##### Endpoint: /api/guest_rud/<guest_id>/
##### Methods: GET, PUT, PATCH, DELETE
###### Description:
* Retrieves details of a specific guest registration for an event created by the authenticated user.
* Allows the authenticated user to update or delete the guest registration.
* Ensures that users can only access and modify guest registrations associated with events they created.

### Permissions
* EventListCreate and EventRetrieveUpdateDestroy:
* Only authenticated users can access these endpoints.
* GuestListCreate and GuestRetrieveUpdateDestroy:
* Only authenticated users can access these endpoints.
* Users can only register guests or modify registrations for events they created.

### API Endpoints

##### Event List and Create:
* Use the /api/event_lc/ 
* endpoint to retrieve a list of events or create a new event.
  
##### Event Retrieve, Update, and Delete:
* Access details of a specific event or update/delete it using the /api/event_rud/<event_id>/
  
##### Guest List and Create:
* Retrieve a list of guest registrations for an event or register new guests using /api/guest_lc/<event_id>/
  
##### Guest Retrieve, Update, and Delete:
* Access details of a specific guest registration or update/delete it using /api/guest_rud/<guest_id>/

### Dependencies
- Django
- Django Rest Framework
- Python
- Git

### Clone the repository:

* git clone https://github.com/sagorluc/Event-Registration-System.git
* cd Event-Registration-System


### Create a virtual environment:
virtualenv vrenv

.\vrenv\Scripts\activate

### Install the project dependencies:
pip install -r requirements.txt

### Set up environment variables:
* pip install python-dotenv
* SECRET_KEY = os.environ.get('SECRET_KEY')

### Apply migrations and create a superuser:
* python manage.py makemigrations
* python manage.py migrate
* python manage.py createsuperuser

### Run the development server:
python manage.py runserver


# Django Template Documentation URL
* Registration Or Sign up: http://127.0.0.1:8000/accounts/register/
* Login: http://127.0.0.1:8000/accounts/login/
 

# Acknowledgments
* [Django Documentation]('https://docs.djangoproject.com/en/3.2/')
* [Django Rest Framework Documentation]('https://www.django-rest-framework.org/')
* [Git Documentation]('https://git-scm.com/doc')

# Contributors
* [Md. Sagar Ali]('https://www.linkedin.com/in/mdsagarali/')