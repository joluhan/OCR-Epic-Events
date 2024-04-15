# Description: This file contains the custom permissions that are used to restrict access to certain views based on the user's role.
from django.core.management.base import CommandError # Importing CommandError from django.core.management.base
from EpicEvents.auth_utils import load_token, validate_token # Importing load_token and validate_token from epicevents.auth_utils
import json
from functools import wraps
from EpicEvents.models import Client, Contract, Event, User


def require_login(command_func): 
    # function to ensur the user is logged in
    def wrapper(*args, **kwargs): # Definition of wrapper function
        token = load_token() # Load the token from the .token file

        if token[0] is None:
            raise CommandError("User not logged in. Please log in.")
        
        user = validate_token(token) # Validate the token

        if user is None:
            raise CommandError("Invalid token. Please log in.")

        return command_func(*args, **kwargs) # Return the command function

    return wrapper

def get_user_role_from_token():
    # get role of the logged in user from .token
    try:
        with open('.token', 'r') as token_file:
            data = json.load(token_file)
            return data.get('user_role', '')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ''


def get_user_id_from_token():
    # get id of the logged in user from .token
    try:
        with open('.token', 'r') as token_file:
            data = json.load(token_file)
            return data.get('user_id', '')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ''
    

def is_management_team(view_func):
    # Permissions which ensure that the employee is part of the management team
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = get_user_role_from_token()
        if user_role != "management":
            raise CommandError("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_sales_team(view_func):
    # Permissions to ensure that the employee is part of the sales team
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = get_user_role_from_token()
        if user_role != "sales":
            raise CommandError("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_sales_team_and_client_rep(view_func):
    # Permissions to ensure that the employee is part of the sales team and is associated with the client
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # check user role
        user_role = get_user_role_from_token()
        if user_role != "sales":
            raise CommandError("You do not have permission to perform this action.")

        # check if user is associated with the client
        user_id = get_user_id_from_token()
        client_id = kwargs.get('client_id')

        try:
            client = Client.objects.get(id=client_id, sales_rep=user_id)
        except Client.DoesNotExist:
            raise CommandError("Access denied. You are not the Sales Representative assigned to this client.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def is_contract_sales_rep_or_is_management_team(view_func):
    # Permission that ensures the user is the sales rep for the contract or a member of the management team
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # check user role
        user_role = get_user_role_from_token()
        user_id = get_user_id_from_token()

        if user_role == "sales":
            # check if user is the sales rep to the contract client
            contract_id = kwargs['contract_id']

            try:
                contract = Contract.objects.get(id=contract_id, sales_rep=user_id)
            except Contract.DoesNotExist:
                raise CommandError("Access denied. You are not the sales person assigned to this contract.")
        elif user_role == "management":
            pass # grant access if the user is part of the management team
        else:
            raise CommandError("You do not have permission to perform this action.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def require_sales_event_access(views_func):
    # Permission which ensures that the sales person is indeed linked to the customer of the contract
    @wraps(views_func)
    def _wrapped_view(request, *args, **kwargs):
        # check user role
        user_role = get_user_role_from_token()
        if user_role != "sales":
            raise CommandError("You do not have permission to perform this action.")
        # Checks if the user is associated with the event client
        user_id = get_user_id_from_token()
        contract_id = kwargs.get('contract_id')

        try:
            contract = Contract.objects.get(id=contract_id, sales_rep=user_id)
        except Contract.DoesNotExist:
            raise CommandError("Access denied. You are not the sales person assigned to this event.")

        return views_func(request, *args, **kwargs)

    return _wrapped_view


def is_event_support_or_is_management_team(view_func):
    # Permission that ensures the user is support staff for the event or a member of the management team
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = get_user_role_from_token()

        if user_role == "support":
            user_id = get_user_id_from_token()
            event_id = kwargs['event_id']

            try:
                event = Event.objects.get(id=event_id, support_staff=user_id)
            except Event.DoesNotExist:
                raise CommandError("Access denied. You are not the Support staff assigned to this event.")

        elif user_role == "management":
            pass # grant access if the user is part of the management team
        else:
            raise CommandError("You do not have permission to perform this action.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
