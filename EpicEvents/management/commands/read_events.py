from django.core.management.base import BaseCommand
from EpicEvents.models import Event
from tabulate import tabulate
from EpicEvents.permissions import require_login


class Command(BaseCommand):
    """A management command to read events. This command is accessible to all users."""

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, nargs='?', help='Event ID to display')
        parser.add_argument('--contract_id', type=int, help='Filter events by contract (ID)', required=False)
        parser.add_argument('--name', type=str, help='Filter events by name', required=False)
        parser.add_argument('--start_date', type=str, help='Filter events by start date (format : YYYY-MM ou YYYY-MM-DD)', required=False)
        parser.add_argument('--end_date', type=str, help='Filter events by end date (format : YYYY-MM ou YYYY-MM-DD)', required=False)
        parser.add_argument('--support_staff', type=str, help='Filter events by support staff (name or ID)', required=False)
        parser.add_argument('--location', type=str, help='Filter events by  location', required=False)
        parser.add_argument('--num_of_participants', type=str, help='Filter events by number of participants (ex: -50, +50, +100, +200)', required=False)

    @require_login
    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']
        contract_filter = kwargs['contract_id']
        name_filter = kwargs['name']
        start_date_filter = kwargs['start_date']
        end_date_filter = kwargs['end_date']
        support_filter = kwargs['support_staff']
        location_filter = kwargs['location']
        participants_filter = kwargs['num_of_participants']

        if event_id is not None:
            try:
                event = Event.objects.get(pk=event_id)
                self.print_event_details([event])
            except Event.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"No event found with ID {event_id}."))
        else:
            events = Event.objects.all()

            if contract_filter:
                events = events.filter(contract__id=contract_filter)

            if name_filter:
                events = events.filter(name__icontains=name_filter)

            if start_date_filter:
                events = events.filter(start_date__icontains=start_date_filter)

            if end_date_filter:
                events = events.filter(end_date__icontains=end_date_filter)

            if support_filter:
                try:
                    support_id = int(support_filter)
                    events = events.filter(support_staff__id=support_id)
                except ValueError:
                    events = events.filter(support_staff__fullname__icontains=support_filter)

            if location_filter:
                events = events.filter(location__icontains=location_filter)

            if participants_filter:
                # filter events based on number of participants
                if participants_filter == '-50':
                    events = events.filter(attendees__lt=50)
                elif participants_filter == '+50':
                    events = events.filter(attendees__gte=50)
                elif participants_filter == '+100':
                    events = events.filter(attendees__gte=100)
                elif participants_filter == '+200':
                    events = events.filter(attendees__gte=200)

            if events.exists():
                self.print_event_details(events)
            else:
                self.stdout.write(self.style.SUCCESS("No events found."))

    def print_event_details(self, events):
        headers = ["ID", "Contract", "Name", "Start Date", "End Date", "Support Staff",
                   "Location", "Number of Participants", "Notes"]
        rows = []

        for event in events:
            row = [
                event.id,
                event.contract,
                event.name,
                event.start_date,
                event.end_date,
                event.support_staff,
                event.location,
                event.attendees,
                event.notes
            ]
            rows.append(row)

        title = "List of Events"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        print(table_with_title)
