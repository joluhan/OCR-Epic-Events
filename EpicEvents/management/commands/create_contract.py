from django.core.management.base import BaseCommand
from EpicEvents.models import Contract, User, Client
from EpicEvents.permissions import is_management_team, require_login

class Command(BaseCommand):
    """A management command to create a contract. This command is only accessible to management team members."""

    def add_arguments(self, parser):
        parser.add_argument('--client_id', type=int, help='Clients ID')
        parser.add_argument('--sales_rep_id', type=int, help='Sales Rep ID')
        parser.add_argument('--total_amount', type=float, help='Total amount')
        parser.add_argument('--amount_remaining', type=float, help='Amount remaining')
        parser.add_argument('--status', type=str, help='Contract status')

    @require_login
    @is_management_team
    def handle(self, *args, **kwargs):
        if kwargs['client_id'] and kwargs['sales_rep_id'] and kwargs['total_amount'] and kwargs['amount_remaining'] and kwargs['status']:
            client_id = kwargs['client_id']
            sales_rep_id = kwargs['sales_rep_id']
            total_amount = kwargs['total_amount']
            amount_remaining = kwargs['amount_remaining']
            status = kwargs['status']
        else:
            client_id = int(input("ID of the client associated with this contract (integer): "))
            sales_rep_id = int(input("ID of the Sales rep attached to this contract (integer): "))
            total_amount = float(input("Total amount to be paid for the contract: "))
            amount_remaining = float(input("Amount remaining to be paid for the contract: "))
            status = input("Status of the contract (waiting for signature, signed, in progress, finished, terminated, cancelled): ").lower()  # convert status to lowercase

        valid_status = [choice[0] for choice in Contract.STATUS_CHOICES]
        if status not in valid_status:
            self.stdout.write(self.style.ERROR(f"The status '{status}' is invalid. Choose from the following options: {', '.join(valid_status)}"))
            return

        # check if client and sales rep with given IDs exist
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"No clients found with ID {client_id}."))
            return

        try:
            sales_rep = User.objects.get(pk=sales_rep_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"No sales team member found with ID {sales_rep_id}."))
            return

        # check if employee role is sales
        if sales_rep.role != 'sales':
            self.stdout.write(self.style.ERROR(f"The employee with the ID {sales_rep_id} does not have the role 'sales'."))
            return

        contract = Contract.objects.create(
            client=client,
            sales_rep=sales_rep,
            total_amount=total_amount,
            amount_remaining=amount_remaining,
            status=status
        )

        self.stdout.write(self.style.SUCCESS(f"Contract {contract.id} created sucessfully."))
