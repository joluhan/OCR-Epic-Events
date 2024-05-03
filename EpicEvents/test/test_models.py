from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from EpicEvents.models import Client, Contract, Event

# Get the custom User model
User = get_user_model()

class UserModelTestCase(TestCase):
    
    def test_create_user(self):
        # Create a user instance
        user = User.objects.create_user(username='testuser', password='Unit123!', role='management', fullname='testuser')
        # Check if the user has been created and has the correct attributes
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'management')
        self.assertEqual(user.fullname, 'testuser')
        # Check if the password is set correctly (password should not be stored in plain text)
        self.assertTrue(user.check_password('Unit123!'))

class ClientModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='salesrep', password='Sales123!', role='sales', fullname='Sales Rep')

    def test_create_client(self):
        # Create a client instance
        client = Client.objects.create(
            sales_rep=self.user,
            fullname="John Doe",
            email="john@doe.com",
            phone="1234567890",
            company_name="Doe Enterprises"
        )
        # Verify that the client was created with correct attributes
        self.assertEqual(client.fullname, "John Doe")
        self.assertEqual(client.email, "john@doe.com")
        self.assertEqual(client.phone, "1234567890")
        self.assertEqual(client.company_name, "Doe Enterprises")
        self.assertEqual(client.sales_rep, self.user)

class ContractModelTestCase(TestCase):
    def setUp(self):
        # Create a test user and client
        self.user = User.objects.create_user(username='salesrep', password='Sales123!', role='sales', fullname='Sales Rep')
        self.client = Client.objects.create(
            sales_rep=self.user,
            fullname="John Doe",
            email="john@doe.com",
            phone="1234567890",
            company_name="Doe Enterprises"
        )

    def test_create_contract(self):
        # Create a contract instance
        contract = Contract.objects.create(
            client=self.client,
            total_amount=1000.0,
            amount_remaining=1000.0,
            status='waiting for signature'
        )
        # Verify that the contract was created with correct attributes
        self.assertEqual(contract.client, self.client)
        self.assertEqual(contract.total_amount, 1000.0)
        self.assertEqual(contract.amount_remaining, 1000.0)
        self.assertEqual(contract.status, 'waiting for signature')

class EventModelTestCase(TestCase):
    def setUp(self):
        # Create a test user, client and contract
        self.user = User.objects.create_user(username='supportrep', password='Support123!', role='support', fullname='Support Rep')
        self.client = Client.objects.create(
            sales_rep=self.user,
            fullname="John Doe",
            email="john@doe.com",
            phone="1234567890",
            company_name="Doe Enterprises"
        )
        self.contract = Contract.objects.create(
            client=self.client,
            total_amount=1000.0,
            amount_remaining=1000.0,
            status='waiting for signature'
        )

    def test_create_event(self):
        # Create an event instance
        event_date = timezone.now().date()
        event = Event.objects.create(
            contract=self.contract,
            name="Annual Meeting",
            start_date=event_date,
            end_date=event_date + timezone.timedelta(days=1),
            support_staff=self.user,
            location="Conference Room 1",
            attendees=50,
            notes="Annual general meeting for stakeholders."
        )
        # Verify that the event was created with correct attributes
        self.assertEqual(event.contract, self.contract)
        self.assertEqual(event.name, "Annual Meeting")
        self.assertEqual(event.start_date, event_date)
        self.assertEqual(event.end_date, event_date + timezone.timedelta(days=1))
        self.assertEqual(event.support_staff, self.user)
        self.assertEqual(event.location, "Conference Room 1")
        self.assertEqual(event.attendees, 50)
        self.assertEqual(event.notes, "Annual general meeting for stakeholders.")
