from django.core.management.base import BaseCommand
from EpicEvents.models import Event, User
from datetime import datetime
from EpicEvents.permissions import require_login, is_event_support_or_is_management_team


class Command(BaseCommand):
    """A management command to modify an event. This command is only accessible to event support team members."""

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='ID of event to be modified')
        parser.add_argument('--name', type=str, help='New name', required=False)
        parser.add_argument('--start_date', type=str, help='New start date (format YYYYMMDD)', required=False)
        parser.add_argument('--end_date', type=str, help='New end date (format YYYYMMDD)', required=False)
        parser.add_argument('--location', type=str, help='New location', required=False)
        parser.add_argument('--num_of_participants', type=int, help='New number of participants', required=False)
        parser.add_argument('--notes', type=str, help='New notes', required=False)
        parser.add_argument('--support_staff_id', type=int, help='ID of new support_staff', required=False)

    @require_login
    @is_event_support_or_is_management_team
    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']
        name = kwargs['name']
        start_date = kwargs['start_date']
        end_date = kwargs['end_date']
        location = kwargs['location']
        num_of_participants = kwargs['num_of_participants']
        notes = kwargs['notes']
        support_staff_id = kwargs['support_staff_id']

        try:
            event = Event.objects.get(pk=event_id)
        except event.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Event with ID {event_id} does not exist."))
            return

        if name:
            event.name = name

        if start_date:
            # convert date to datetime objet
            event.start_date = datetime.strptime(start_date, '%Y%m%d')

        if end_date:
            # convert date to datetime objet
            event.end_date = datetime.strptime(end_date, '%Y%m%d')

        if location:
            event.location = location

        if num_of_participants is not None:
            event.attendees = num_of_participants

        if notes:
            event.notes = notes

        if support_staff_id is not None:
            try:
                support_staff = User.objects.get(pk=support_staff_id, role='support')
                event.support_staff = support_staff
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("user with the specified ID does not exist or is not a support team member."))
                return

        event.save()

        self.stdout.write(self.style.SUCCESS(f"Évent with ID {event_id} modified sucessfully."))
