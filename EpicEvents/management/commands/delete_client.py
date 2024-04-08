from django.core.management.base import BaseCommand
from EpicEvents.models import Client
from EpicEvents.permissions import require_login, is_sales_team_and_client_rep


class Command(BaseCommand):
    """A management command to delete a client. This command is only accessible to sales team members."""

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID of client to delete')

    @require_login
    @is_sales_team_and_client_rep
    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']

        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            self.stdout.write(self.style.SUCCESS(f"Client with ID {client_id} deleted successfully"))
        except Client.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Client with ID {client_id} not found"))
