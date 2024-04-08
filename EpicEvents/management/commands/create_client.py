from django.core.management.base import BaseCommand
from EpicEvents.models import Client, User
from django.utils import timezone
from EpicEvents.permissions import require_login, is_sales_team, get_user_id_from_token


class Command(BaseCommand):
    """A management command to create a client. This command is only accessible to sales team members."""

    @require_login
    @is_sales_team
    def handle(self, *args, **kwargs):
        fullname = input('Clients full name: ')
        email = input('Clients email: ')
        phone = input("Client's phone number: ")
        company_name = input("Client's company name: ")
        created_at = timezone.now()

        sales_rep_id = get_user_id_from_token()
        try:
            sales_rep = User.objects.get(id=sales_rep_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"User with ID {sales_rep_id} does not exist."))
            return

        client = Client.objects.create(
                sales_rep=sales_rep,
                fullname=fullname, 
                email=email, 
                phone=phone,
                company_name=company_name, 
                created_at=created_at,
                # updated_at=updated_at
            )

        self.stdout.write(self.style.SUCCESS(f"Client '{fullname}' created successfully. Client ID: {client.id}"))
