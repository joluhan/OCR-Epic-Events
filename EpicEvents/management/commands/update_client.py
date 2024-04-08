from django.core.management.base import BaseCommand
from EpicEvents.models import Client
from EpicEvents.permissions import require_login, is_sales_team_and_client_rep


class Command(BaseCommand):
    """A management command to update a client."""

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID of client to modify')
        parser.add_argument('--fullname', type=str, help='Ner full name of client', required=False)
        parser.add_argument('--email', type=str, help='New email of client', required=False)
        parser.add_argument('--phone', type=str, help='New phone number of client', required=False)
        parser.add_argument('--company_name', type=str, help='New company name of client', required=False)

    @require_login
    @is_sales_team_and_client_rep
    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']

        try:
            client = Client.objects.get(pk=client_id)

            if kwargs['fullname']:
                client.fullname = kwargs['fullname']
            if kwargs['email']:
                client.email = kwargs['email']
            if kwargs['phone']:
                client.phone = kwargs['phone']
            if kwargs['company_name']:
                client.company_name = kwargs['company_name']

            client.save()
            self.stdout.write(self.style.SUCCESS(f"Client with ID {client_id} modified successfully."))
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Client with ID {client_id} does not exist."))
