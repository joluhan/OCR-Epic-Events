from django.core.management.base import BaseCommand
from EpicEvents.models import Event
from EpicEvents.permissions import require_login, is_event_support_or_is_management_team


class Command(BaseCommand):
    """A management command to delete an event. This command is only accessible to event support team members."""

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='ID of event to delete')

    @require_login
    @is_event_support_or_is_management_team
    def handle(self, *args, **options):
        event_id = options['event_id']

        try:
            event = Event.objects.get(pk=event_id)
            event.delete()
            self.stdout.write(self.style.SUCCESS(f"Évent with ID {event_id} deleted sucessfully."))
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Event with ID {event_id} does not exist."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Uno error has occurred: {e}"))
