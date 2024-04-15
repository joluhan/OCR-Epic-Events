from django.core.management.base import BaseCommand
import getpass
from EpicEvents.models import User
from EpicEvents.permissions import is_management_team, require_login

class Command(BaseCommand):
    """A management command to create a new user. 
    The user is prompted to enter the user's full name, username, role and password. 
    The role must be one of the following: sales, support or management. 
    The user is then created and saved to the database."""
    @require_login # only logged in users can run this command
    @is_management_team # only management team members can run this command
    def handle(self, *args, **options):
        fullname = input("User's full name: ")
        username = input("User's username: ")
        role = input("Users role (sales, support or management): ")
        password = getpass.getpass('password: ')
        role = role.lower()

        # verify that the role is a valid choice
        valid_roles = [r[0] for r in User.ROLE_CHOICES] # get the valid roles
        if role not in valid_roles:
            # print error message
            self.stdout.write(self.style.ERROR(f"The role '{role}' is invalid. Use one of the following : {', '.join(valid_roles)}"))
            return

        # print the inputs
        self.stdout.write(self.style.SUCCESS(f"Inputs: {fullname}, {role}, {username}"))

        user = User.objects.create_user(
                username=username, 
                password=password,
                fullname=fullname, 
                role=role
            )
        
        # print success message
        self.stdout.write(self.style.SUCCESS(f"User created successfully: {user}"))
