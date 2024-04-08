from django.core.management.base import BaseCommand
from EpicEvents.models import Contract
from EpicEvents.permissions import require_login, is_management_team


class Command(BaseCommand):
    """A management command to delete a contract. This command is only accessible to management team members."""

    def add_arguments(self, parser):
        parser.add_argument('contract_id', type=int, help='ID of contract to delete')

    @require_login
    @is_management_team
    def handle(self, *args, **options):
        contract_id = options['contract_id']

        try:
            contract = Contract.objects.get(pk=contract_id)
            contract.delete()
            self.stdout.write(self.style.SUCCESS(f"contract with ID {contract_id} deleted sucessfully."))

        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"contract with ID {contract_id} does not exist"))
            return
