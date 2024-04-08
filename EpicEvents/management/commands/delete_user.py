from django.core.management.base import BaseCommand
from EpicEvents.models import User
from EpicEvents.permissions import require_login, is_management_team


class Command(BaseCommand):
    """A management command to delete a user. 
    The user is prompted to enter the ID of the user to delete. The user is then deleted from the database."""
    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID of user to delete')

    @require_login
    @is_management_team
    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f"User with ID {user_id} deleted sucessfully"))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"User with ID {user_id} not found"))
