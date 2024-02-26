from event.models import MultipleToken, CreateEvent
import random
import string

def generate_token(length=10):
    # Generate a random token number
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return token
            
def create_tokens_for_event(event, num_tokens=1):
    # Create and associate token numbers with the event
    tokens = []
    # event_token = TokenNumber.objects.create(event=event)  # Create a single TokenNumber instance for the event
    event_token = CreateEvent.objects.get(pk=event.pk) # create instance
    for _ in range(num_tokens):
        token_number = generate_token()  # Generate a unique token number
        token = MultipleToken.objects.create(number=token_number)
        event_token.token_numbers.add(token)  # Associate the token with the event
        tokens.append(token_number)
    return tokens