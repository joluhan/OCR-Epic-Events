from django.core.management.base import BaseCommand
from EpicEvents.models import Contract, User
from EpicEvents.permissions import require_login, is_contract_sales_rep_or_is_management_team


class Command(BaseCommand):
    """A management command to update a contract."""

    def add_arguments(self, parser):
        parser.add_argument('contract_id', type=int, help='ID of contract to modify')
        parser.add_argument('--total_amount', type=float, help='New total amount', required=False)
        parser.add_argument('--amount_remaining', type=float, help='New amount remainig')
        parser.add_argument('--status', type=str, help='New status')
        parser.add_argument('--sales_rep_id', type=int, help='ID of new sales_rep', required=False)

    @require_login
    @is_contract_sales_rep_or_is_management_team
    def handle(self, *args, **kwargs):
        contract_id = kwargs['contract_id']
        total_amount = kwargs['total_amount']
        amount_remaining = kwargs['amount_remaining']
        status = kwargs['status'].lower()
        sales_rep_id = kwargs['sales_rep_id']

        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Contract with ID {contract_id} does not exist."))
            return

        if sales_rep_id != None and sales_rep_id != '':
            try:
                sales_rep = User.objects.get(pk=sales_rep_id, role='sales')
                contract.sales_rep = sales_rep
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("The user with the specified ID does not exist or != a member of sales team."))
                return

        if total_amount != None and total_amount != '':
            contract.total_amount = total_amount

        if amount_remaining != None and amount_remaining != '':
            contract.amount_remaining = amount_remaining

        if status != None and status != '':
            valid_status = [choice[0] for choice in Contract.STATUS_CHOICES]
            if status not in valid_status:
                self.stdout.write(self.style.ERROR(f"Status '{status}' is invalid. Use any of the following: {', '.join(valid_status)}"))
                return
            contract.status = status

        contract.save()

        self.stdout.write(self.style.SUCCESS(f"contract with ID {contract_id} modified susseccfully."))

