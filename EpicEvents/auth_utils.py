import jwt  # Importing the jwt library to encode and decode JWT tokens.
import json  # Importing the json library for reading and writing data in JSON format.
import os  # Importing the os library to interact with the operating system, e.g., for file handling.
from django.conf import settings  # Importing Django's settings to access project settings.
from datetime import datetime, timezone  # Importing datetime to work with dates and times.
from EpicEvents.models import User  # Importing the User model from the epicevents app.

TOKEN_FILE_PATH = ".token" # Defining the path to the file where the token will be stored.

# Function to load an authentication token from a file.
def load_token():
    try:
        # Attempting to open the token file in read mode.
        with open(TOKEN_FILE_PATH, 'r') as token_file:
            data = json.load(token_file) # Loading the JSON data from the file.
            # Returning the token and its expiration time as a datetime object.
            return data['token'], datetime.fromtimestamp(data['expiration_time'], timezone.utc)
    except(FileNotFoundError, json.JSONDecodeError, KeyError):
        # If file is not found, JSON is invalid, or expected key is missing, return None for both values.
        return None, None
    

# Function to generate a new authentication token for a user.
def generate_token(user, expiration_time):
    # Encoding a new JWT token with user's ID and expiration time.
    token = jwt.encode({
            'user_id': user.id, 
            'exp': expiration_time
        }, settings.TOKEN_KEY, algorithm='HS256')
    
    # Opening the token file in write mode to save the token.
    with open(TOKEN_FILE_PATH, 'w') as token_file:
        # Writing the token and related information as JSON to the file.
        token_file.write(json.dumps({
                    'token': token,
                    'expiration_time': expiration_time.timestamp(), # Converting expiration_time to a timestamp.
                    'user_id': user.id,
                    'user_role': user.role,
                    'user_name': user.fullname,
                }))
    return token # Returning the generated token.


# Function to validate an existing token.
def validate_token(token):
    token, expiration_time = load_token()
    print("expiration time,", expiration_time)
    print("utc time,", datetime.now(timezone.utc))
    print("expiration time > time: ", expiration_time > datetime.now(timezone.utc))

    # Checking if token exists, has an expiration time, and is not yet expired.
    if token and expiration_time and expiration_time > datetime.now(timezone.utc):
        try:
            # Decoding the token to verify its validity and extract payload.
            payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=['HS256'])
            print(payload) # Printing the payload for debugging or logging purposes.
            user_id = payload['user_id'] # Extracting user_id from the payload.
            user = User.objects.get(id=user_id) # Retrieving the user object by its ID.
            return user # Returning the user object if token is valid and user exists.
        except jwt.ExpiredSignatureError:
            # If the token is expired, delete the token file.
            os.remove(TOKEN_FILE_PATH)
            return None # Returning None to indicate token is no longer valid.
        except jwt.InvalidTokenError:
            # If the token is invalid for any reason other than being expired, return None.
            return None
        except User.DoesNotExist:
            # If the user does not exist, return None.
            return None
    return None # Returning None if token is not found, expired, or invalid for any reason.
