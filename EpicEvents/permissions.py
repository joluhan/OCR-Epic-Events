# Description: This file contains the custom permissions that are used to restrict access to certain views based on the user's role.
from django.core.management.base import CommandError # Importing CommandError from django.core.management.base
from EpicEvents.auth_utils import load_token, validate_token # Importing load_token and validate_token from epicevents.auth_utils
import json # Importing json
from functools import wraps # Importing wraps from functools
from EpicEvents.models import Client, Contract, Event, User # Importing Client, Contract, Event, and User from epicevents.models

# Function to require login for a command function
def require_login(command_func): # Definition of require_login function
    # function to ensur the user is logged in
    def wrapper(*args, **kwargs): # Definition of wrapper function
        token = load_token() # Load the token from the .token file

        if not token: # If the token is not found
            raise CommandError("user not logged in. please log in.") # Raise a CommandError
        
        user = validate_token(token) # Validate the token

        if user is None: # If the user is not found
            raise CommandError("Invalid token. Please log in.") # Raise a CommandError

        return command_func(*args, **kwargs) # Return the command function

    return wrapper # Return the wrapper function
