from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import User, Contract, Client, Event
from unittest.mock import patch, Mock
from datetime import datetime, timedelta, timezone
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_update_event_successful(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="management"
    )

    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a dummy sales for the test
    sales = User.objects.create_user(
        username='testsales',
        password='testpassword', 
        fullname='Test sales', 
        role='sales'
        )

    # Create a fictitious contract for the test
    contract = Contract.objects.create(
        client_id=client.id, 
        sales_rep_id=sales.id, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy support for the test
    support_user = User.objects.create(
        fullname='test support',
        username='testsupport',
        role='support'
        )

    event = Event.objects.create(
        contract=contract, 
        name='Test event', 
        start_date='2024-06-01',
        end_date='2024-06-05', 
        support_staff=support_user,
        location='location test', 
        attendees=50, 
        notes='Notes test'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='management')

        # Mock the load_token function to return a valid token
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

    # Capturing standard output for verification
    call_command('update_event', int(event.id), '--name', 'New event name')

    # Verifying that the user was successfully modified
    user.refresh_from_db()
    captured = capsys.readouterr()
    assert f"Event with ID {event.id} modified sucessfully." in captured.out


@pytest.mark.django_db
def test_update_event_permission_failure(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="sales"
    )

    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a dummy sales for the test
    sales = User.objects.create_user(
        username='testsales',
        password='testpassword', 
        role='sales'
        )

    # Create a fictitious contract for the test
    contract = Contract.objects.create(
        client_id=client.id, 
        sales_rep_id=sales.id, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy support for the test
    support_user = User.objects.create(
        fullname='test support', 
        username='testsupport', 
        role='support'
        )

    event = Event.objects.create(
        contract=contract, 
        name='Test event', 
        start_date='2024-06-01',
        end_date='2024-06-05', 
        support_staff=support_user,
        location='location test', 
        attendees=50, 
        notes='Notes test'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')

        # Mock the load_token function to return a valid token
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            
            try:
                # Capturing standard output for verification
                call_command('update_event', int(event.id), '--name', 'New Name')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_event_not_found(mocker, capsys):
    # Create a dummy user for the test (role: 'management')
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='management'
        )

    # ID of an event that does not exist
    event_id = 999

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='management')

        # Mock the load_token function to return a valid token
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('update_event', int(event_id), '--name', 'New event')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == f"Event with ID {event_id} does not exist."
