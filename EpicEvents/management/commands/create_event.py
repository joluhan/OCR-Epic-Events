from django.core.management.base import BaseCommand, CommandError
from EpicEvents.models import Event, Contract, User
from datetime import datetime
from EpicEvents.permissions import is_sales_team, require_login


class Command(BaseCommand):
    """A management command to create an event. This command is only accessible to sales team members."""

    @require_login
    @is_sales_team
    def handle(self, *args, **kwargs):
        contract_id = int(input("ID of the Contract linked to the event: "))
        name = input("Name of the event: ")
        start_date = input("Event start date (in YYYYMMDD format): ")
        end_date = input("Event end date (in YYYYMMDD format): ")
        support_staff_id = int(input("ID of the employee assigned to this event (support staff): "))
        location = input("location of the event: ")
        number_of_participants = int(input("Number of participants: "))
        notes = input("Notes for the event: ")

        # check if the contract exists
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist:
            raise CommandError(f"The Contract with ID {contract_id} does not exist.")

        # Checking that the support_staff collaborator exists and has the "support" role
        try:
            support_staff = User.objects.get(pk=support_staff_id, role='support')
        except User.DoesNotExist:
            raise CommandError(f"User with id {support_staff_id} does not exist or is not in role 'support'.")

        # Converting start and end dates
        try:
            start_date = datetime.strptime(start_date, '%Y%m%d').date()
            end_date = datetime.strptime(end_date, '%Y%m%d').date()
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid date format, use the format YYYYMMDD."))
            return

        # create the event
        event = Event.objects.create(
            contract=contract,
            name=name,
            start_date=start_date,
            end_date=end_date,
            support_staff=support_staff,
            location=location,
            attendees=number_of_participants,
            notes=notes
        )

        self.stdout.write(self.style.SUCCESS(f"Event created successfully: {event}"))
