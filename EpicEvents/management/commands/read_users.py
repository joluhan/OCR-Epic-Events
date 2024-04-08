from django.core.management.base import BaseCommand, CommandError
from tabulate import tabulate
from EpicEvents.models import User
from EpicEvents.permissions import require_login


class Command(BaseCommand):
    """A management command to read users."""

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='?', type=int, help='User ID to retrieve')
        parser.add_argument('--fullname', type=str, help='Filter users by fullname', required=False)
        parser.add_argument('--username', type=str, help='Filter users by username', required=False)
        parser.add_argument('--role', type=str, help='Filter users by role', required=False)

    @require_login
    def handle(self, *args, **options):
        user_id = options['user_id']
        fullname_filter = options['fullname']
        username_filter = options['username']
        role_filter = options['role']

        if user_id is not None:
            try:
                user = User.objects.get(id=user_id)
                self.print_users_details([user])
            except User.DoesNotExist:
                raise CommandError(f"user with ID {user_id} not found.")
        else:
            users = User.objects.all()

            if fullname_filter:
                users = users.filter(fullname__icontains=fullname_filter)

            if username_filter:
                users = users.filter(username__icontains=username_filter)

            if role_filter:
                users = users.filter(role__icontains=role_filter)

            if users:
                self.print_users_details(users)
            else:
                self.stdout.write(self.style.SUCCESS("No users found."))

    def print_users_details(self, data):
        headers = ["ID", "Full Name", "Username", "Role"]
        rows = []

        for item in data:
            row = [item.id, item.fullname, item.username, item.role]
            rows.append(row)

        title = "List of users"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        self.stdout.write(table_with_title)
