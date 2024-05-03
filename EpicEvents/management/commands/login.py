from django.core.management.base import BaseCommand
from django.core.management import call_command
# from pytz import timezone
from EpicEvents.auth_utils import generate_token
from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate
import getpass


class Command(BaseCommand):
    """A management command to login a user. The user is prompted to enter their username and password. 
    If the user is authenticated, a token is generated and saved to a file."""

    def handle(self, *args, **options):
        # request login credentials
        username = input("username : ")
        password = getpass.getpass("password : ")

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            expiration_time = datetime.now(timezone.utc) + timedelta(hours=2)
            token = generate_token(user, expiration_time)

            self.stdout.write(self.style.SUCCESS(f'Login successful! Hello : {user.fullname}'))
            call_command('execute', user.role)
        else:
            self.stdout.write(self.style.ERROR('Authentication failed'))
