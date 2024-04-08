from django.core.management.base import BaseCommand, CommandError
from tabulate import tabulate
from EpicEvents.models import Client
from EpicEvents.permissions import require_login


class Command(BaseCommand):
    """A management command to read clients."""

    def add_arguments(self, parser):
        parser.add_argument('client_id', nargs='?', type=int, help='Client ID to retrieve')
        parser.add_argument('--fullname', type=str, help='Filter customers by full name', required=False)
        parser.add_argument('--email', type=str, help='Filter customers by e-mail', required=False)
        parser.add_argument('--phone', type=str, help='Filter customers by phone', required=False)
        parser.add_argument('--company_name', type=str, help='Filter customers by company name', required=False)

    @require_login
    def handle(self, *args, **options):
        client_id = options['client_id']
        fullname_filter = options['fullname']
        email_filter = options['email']
        phone_filter = options['phone']
        company_filter = options['company_name']

        if client_id is not None:
            try:
                client = Client.objects.get(id=client_id)
                self.print_clients_details([client])
            except Client.DoesNotExist:
                raise CommandError(f"Client with ID {client_id} not found.")
        else:
            clients = Client.objects.all()

            if fullname_filter:
                clients = clients.filter(fullname__icontains=fullname_filter)

            if email_filter:
                clients = clients.filter(email__icontains=email_filter)

            if phone_filter:
                clients = clients.filter(phone__icontains=phone_filter)

            if company_filter:
                clients = clients.filter(company__icontains=company_filter)

            if clients:
                self.print_clients_details(clients)
            else:
                self.stdout.write(self.style.SUCCESS("No clients found."))

    def print_clients_details(self, data):
        headers = ["ID", "Full Name", "Email", "Phone", "Company", "Sales rep", "Created at",
                   "Last update"]
        rows = []

        for item in data:
            formatted_created_at = item.created_at.strftime('%Y-%m-%d')
            formatted_updated_at = item.updated_at.strftime('%Y-%m-%d')
            row = [item.id, item.fullname, item.email,
                   item.phone, item.company_name, item.sales_rep,
                   formatted_created_at, formatted_updated_at]
            rows.append(row)

        title = "List of Clients"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        print(table_with_title)
