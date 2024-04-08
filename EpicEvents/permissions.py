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

# Function to ensure the user is part of the management team
def get_user_role_from_token(): # Definition of get_user_role_from_token function
    # get role of the logged in user from .token
    try: # Try block
        with open('.token', 'r') as token_file: # Open the .token file
            data = json.load(token_file) # Load the data from the token file
            return data.get('user_role', '') # Return the user role
    except (FileNotFoundError, json.JSONDecodeError, KeyError): # Except block
        return '' # Return an empty string

# Function to get the user id from the token
def get_user_id_from_token():
    # get id of the logged in user from .token
    try: # Try block
        with open('.token', 'r') as token_file: # Open the .token file
            data = json.load(token_file) # Load the data from the token file
            return data.get('user_id', '') # Return the user id
    except (FileNotFoundError, json.JSONDecodeError, KeyError): # Except block
        return '' # Return an empty string

# Function to ensure the user is part of the management team
def is_management_team(view_func): 
    # Permissions which ensure that the employee is part of the management team
    @wraps(view_func) # Wraps the view function
    def _wrapped_view(request, *args, **kwargs): # Definition of _wrapped_view function
        user_role = get_user_role_from_token() # Get the user role from the token
        if user_role != "management": # If the user role is not management
            raise CommandError("You do not have permission to perform this action.") # Raise a CommandError
        return view_func(request, *args, **kwargs) # Return the view function
    return _wrapped_view # Return the wrapped view

# Function to ensure the user is part of the sales team
def is_sales_team(view_func):
    # Permissions to ensure that the employee is part of the sales team
    @wraps(view_func) # Wraps the view function
    def _wrapped_view(request, *args, **kwargs): # Definition of _wrapped_view function
        user_role = get_user_role_from_token() # Get the user role from the token
        if user_role != "sales": # If the user role is not sales
            raise CommandError("You do not have permission to perform this action.") # Raise a CommandError
        return view_func(request, *args, **kwargs) # Return the view function
    return _wrapped_view # Return the wrapped view

# Function to ensure the user is part of the support team
def is_sales_team_and_client_rep(view_func):
    # Permissions to ensure that the employee is part of the sales team and is associated with the client
    @wraps(view_func) # Wraps the view function
    def _wrapped_view(request, *args, **kwargs): # Definition of _wrapped_view function
        # check user role from token
        user_role = get_user_role_from_token() # Get the user role from the token
        if user_role != "sales": # If the user role is not sales
            raise CommandError("You do not have permission to perform this action.") # Raise a CommandError

        # check if user is associated with the client
        user_id = get_user_id_from_token() # Get the user id from the token
        client_id = kwargs.get('client_id') # Get the client id from the arguments

        try: # Try block
            client = Client.objects.get(id=client_id, sales_rep=user_id) # Get the client from the client id
        except Client.DoesNotExist: # Except block
            raise CommandError("Access denied. You are not the Sales Representative assigned to this client.") # Raise a CommandError

        return view_func(request, *args, **kwargs) # Return the view function

    return _wrapped_view # Return the wrapped view

def is_contract_sales_rep_or_is_management_team(view_func):
    # Permission that ensures the user is the sales rep for the contract or a member of the management team
    @wraps(view_func) # Wraps the view function
    def _wrapped_view(request, *args, **kwargs): # Definition of _wrapped_view function
        # check user role
        user_role = get_user_role_from_token() # Get the user role from the token
        user_id = get_user_id_from_token() # Get the user id from the token

        if user_role == "sales": # If the user role is sales
            # check if user is the sales rep to the contract client
            contract_id = kwargs['contract_id'] # Get the contract id from the arguments

            try:
                contract = Contract.objects.get(id=contract_id, sales_rep=user_id) # Get the contract from the contract id
            except Contract.DoesNotExist: # Except block
                raise CommandError("Access denied. You are not the sales person assigned to this contract.") # Raise a CommandError
        elif user_role == "management": # If the user role is management
            pass # grant access if the user is part of the management team
        else:
            raise CommandError("You do not have permission to perform this action.") # Raise a CommandError

        return view_func(request, *args, **kwargs) # Return the view function

    return _wrapped_view # Return the wrapped view

def require_sales_event_access(views_func):
    # Permission which ensures that the sales person is indeed linked to the customer of the contract
    @wraps(views_func) # Wraps the view function
    def _wrapped_view(request, *args, **kwargs): # Definition of _wrapped_view function
        # check user role
        user_role = get_user_role_from_token() 
        if user_role != "sales": # If the user role is not sales
            raise CommandError("You do not have permission to perform this action.") # Raise a CommandError
        # Checks if the user is associated with the event client
        user_id = get_user_id_from_token() # Get the user id from the token
        contract_id = kwargs.get('contract_id') # Get the contract id from the arguments

        try:
            contract = Contract.objects.get(id=contract_id, sales_rep=user_id) # Get the contract from the contract id
        except Contract.DoesNotExist: # Except block
            raise CommandError("Access denied. You are not the sales person assigned to this event.") # Raise a CommandError

        return views_func(request, *args, **kwargs) # Return the view function

    return _wrapped_view # Return the wrapped view

def is_event_support_or_is_management_team(view_func):
    # Permission that ensures the user is support staff for the event or a member of the management team
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs): # Definition of _wrapped_view function
        user_role = get_user_role_from_token() # Get the user role from the token

        if user_role == "support": # If the user role is support
            user_id = get_user_id_from_token() # Get the user id from the token
            event_id = kwargs['event_id'] # Get the event id from the arguments

            try:
                event = Event.objects.get(id=event_id, support_staff=user_id) # Get the event from the event id
            except Event.DoesNotExist: # Except block
                raise CommandError("Access denied. You are not the Support staff assigned to this event.") # Raise a CommandError

        elif user_role == "management": # If the user role is management
            pass # grant access if the user is part of the management team
        else:
            raise CommandError("You do not have permission to perform this action.") # Raise a CommandError

        return view_func(request, *args, **kwargs) # Return the view function

    return _wrapped_view # Return the wrapped view
