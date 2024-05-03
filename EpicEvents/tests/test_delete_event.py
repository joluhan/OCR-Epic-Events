import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import Event, User, Client, Contract
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, Mock


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_delete_event_success(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a fictitious user management for the test
    management_user = User.objects.create_user(
        username='test_user_management',
        password='testpassword',
        fullname='Test management user',
        role='management'
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
        client=client, 
        sales_rep=sales, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy event for the test
    event = Event.objects.create(
        contract=contract, 
        name='event Test',
        start_date=datetime.now(),
        end_date='2024-12-05',
        support_staff=management_user,
        location='location test',
        attendees=50,
        notes='notes test'
        )

    # Create a dummy user for testing
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='support'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='support')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            call_command('delete_event', int(event.pk))

            # Checking the success message
            assert f"Event with ID {event.pk} deleted sucessfully." in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_delete_event_permission_denied(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a fictitious user management for the test
    management_user = User.objects.create_user(
        username='test_user_management',
        password='testpassword',
        fullname='Test management user',
        role='management'
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
        client=client, 
        sales_rep=sales, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy event for the test
    event = Event.objects.create(
        contract=contract, 
        name='event Test',
        start_date=datetime.now(),
        end_date='2024-12-05',
        support_staff=management_user,
        location='location test',
        attendees=50,
        notes='notes test'
        )

    # Create a dummy user for testing
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('delete_event', int(event.pk))
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_event_user_not_logged_in(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a fictitious user management for the test
    management_user = User.objects.create_user(
        username='test_user_management',
        password='testpassword',
        fullname='Test management user',
        role='management'
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
        client=client, 
        sales_rep=sales, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy event for the test
    event = Event.objects.create(
        contract=contract, 
        name='event Test',
        start_date=datetime.now(),
        end_date='2024-12-05',
        support_staff=management_user,
        location='location test',
        attendees=50,
        notes='notes test'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to simulate a non-logged user
        mocker.patch('EpicEvents.permissions.load_token', return_value=(None, None))

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('delete_event', int(event.pk))
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "User not logged in. Please log in."


@pytest.mark.django_db
def test_delete_event_event_not_found(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a fictitious user management for the test
    management_user = User.objects.create_user(
        username='test_user_management',
        password='testpassword',
        fullname='Test management user',
        role='management'
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
        client=client, 
        sales_rep=sales, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy event for the test
    event = Event.objects.create(
        contract=contract, 
        name='event Test',
        start_date=datetime.now(),
        end_date='2024-12-05',
        support_staff=management_user,
        location='location test',
        attendees=50,
        notes='notes test'
        )

    # Create a dummy user for testing
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='management')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('delete_event', 9999)
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "Event with ID 9999 does not exist."
