from django.core.management.base import BaseCommand
from EpicEvents.auth_utils import load_token
import os


class Command(BaseCommand):
    """A management command to logout a user. The user's token is deleted from the file system."""

    def handle(self, *args, **options):
        # Load token from file
        token, _ = load_token()

        if token:
            # delete .token file
            os.remove('.token')
            self.stdout.write(self.style.SUCCESS('Logout successful!'))
        else:
            self.stdout.write(self.style.SUCCESS('No tokens found. The user is not logged in.'))
