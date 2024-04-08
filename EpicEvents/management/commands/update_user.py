from django.core.management.base import BaseCommand
from EpicEvents.models import User
from EpicEvents.permissions import require_login, is_management_team


class Command(BaseCommand):
    """A management command to modify a user."""

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID of user to modify')
        parser.add_argument('--fullname', type=str, help='New fullname of user')
        parser.add_argument('--role', type=str, help='New role of user (management, sales, support)')
        parser.add_argument('--username', type=str, help='New username of user')

    @require_login
    @is_management_team
    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        fullname = kwargs['fullname']
        role = kwargs['role']
        new_username = kwargs['username']
        # password = kwargs['password']

        try:
            user = User.objects.get(id=user_id)

            if fullname:
                user.fullname = fullname

            if role:
                user.role = role

            if new_username:
                user.username = new_username

            user.save()
            self.stdout.write(self.style.SUCCESS(f"user with ID {user_id} modified successfully"))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"user with ID {user_id} not found"))
