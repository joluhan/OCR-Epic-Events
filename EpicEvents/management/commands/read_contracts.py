from django.core.management.base import BaseCommand
from tabulate import tabulate
from EpicEvents.models import Contract
from EpicEvents.permissions import require_login


class Command(BaseCommand):
    """A management command to read contracts. This command is accessible to all users."""

    def add_arguments(self, parser):
        parser.add_argument('contract_id', type=int, nargs='?', help='Contract ID to display')
        parser.add_argument('--client', type=str, help='Filter Contracts by client (name or ID)', required=False)
        parser.add_argument('--sales_rep', type=str, help='Filter Contracts by sales rep (name or ID)', required=False)
        parser.add_argument('--total_amount', type=float, help='Filter Contracts total amount', required=False)
        parser.add_argument('--amount_remaining', type=float, help='Filter Contracts by amount remaining', required=False)
        parser.add_argument('--status', type=str, help='Filter Contracts by status (waiting for signature, signed, in progress, finished, terminated, cancelled)', required=False)
        parser.add_argument('--created_at', type=str, help='Filter Contracts by date of création (format : YYYY-MM-DD)', required=False)

    @require_login
    def handle(self, *args, **kwargs):
        contract_id = kwargs['contract_id']
        client_filter = kwargs['client']
        sales_rep_filter = kwargs['sales_rep']
        total_amount_filter = kwargs['total_amount']
        amount_remaining_filter = kwargs['amount_remaining']
        status_filter = kwargs['status']
        created_at_filter = kwargs['created_at']

        if contract_id is not None:
            try:
                contract = Contract.objects.get(pk=contract_id)
                self.print_Contract_details([contract])
            except Contract.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"No Contract found with ID {contract_id}."))
        else:
            contracts = Contract.objects.all()

            if client_filter:
                # ID filtering test
                try:
                    client_id = int(client_filter)
                    contracts = contracts.filter(client__id=client_id)
                except ValueError:
                    # otherwise try filtering by name
                    contracts = contracts.filter(client__fullname__icontains=client_filter)

            if sales_rep_filter:
                # ID filtering test
                try:
                    sales_rep_id = int(sales_rep_filter)
                    contracts = contracts.filter(sales_rep__id=sales_rep_id)
                except ValueError:
                    # otherwise try filtering by name
                    contracts = contracts.filter(sales_rep__fullname__icontains=sales_rep_filter)

            if total_amount_filter:
                contracts = contracts.filter(total_amount=total_amount_filter)

            if amount_remaining_filter:
                contracts = contracts.filter(amount_remaining=amount_remaining_filter)

            if status_filter:
                contracts = contracts.filter(status__icontains=status_filter)

            if created_at_filter:
                contracts = contracts.filter(created_at__icontains=created_at_filter)

            if contracts.exists():
                self.print_Contract_details(contracts)
            else:
                self.stdout.write(self.style.SUCCESS("No Contract found."))

    def print_Contract_details(self, contracts):
        headers = ["ID", "Client", "Sales Rep", "Total Amount", "Amount Remaining", "Status", "Date of création"]
        rows = []

        for contract in contracts:
            row = [contract.id, contract.client, contract.sales_rep, contract.total_amount,
                   contract.amount_remaining, contract.status, contract.created_at]
            rows.append(row)

        title = "List of Contracts"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        print(table_with_title)
