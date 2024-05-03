import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from epicevents.management.commands.create_event import Command
from epicevents.models import Contract, User, Client
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, Mock


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_create_event_success(mocker, custom_input):
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

    # Create a dummy contract for the test
    contract = Contract.objects.create(
        client_id=client.id, 
        sales_rep_id=sales.id, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy support for the test
    support_user = User.objects.create(
        username='testsupport', 
        role='support'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='sales')

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=support_user)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            call_command(
                'create_event', 
                contract_id=contract.id, 
                name='Nom event', 
                start_date='20220101', 
                end_date='20220105',
                support_staff_id=support_user.id, 
                location='Lieu event', 
                number_of_participants=50, 
                notes='Notes event'
                )

            # Checking the success message
            assert "Event created successfully" in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_create_events_permission_failure(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a dummy user for testing (role: 'sales' rather than 'support')
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Create a dummy contract for the test
    contract = Contract.objects.create(
        client_id=client.id, 
        sales_rep_id=user.id, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check (rôle: 'gestion' plutôt que 'sales')
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='gestion')

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            cmd = Command()

            # Calling the command handle function with the correct arguments
            try:
                 cmd.handle(
                contract_id=contract.id, 
                name='Nom event', 
                start_date='2022-01-01', 
                end_date='2022-01-05',
                support_staff_id=user.id, 
                location='Lieu event', 
                number_of_participants=50, 
                notes='Notes event'
                )
                 
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_create_events_unauthenticated_user(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a dummy user for testing (role: 'sales' rather than 'support')
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Create a dummy contract for the test
    contract = Contract.objects.create(
        client_id=client.id, 
        sales_rep_id=user.id, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check (utilisateur non connecté)
        mocker.patch('epicevents.permissions.load_token', return_value=(None, None))

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            cmd = Command()

            # Calling the command handle function with the correct arguments
            try:
                cmd.handle(
                contract_id=contract.id, 
                name='Nom event', 
                start_date='2022-01-01', 
                end_date='2022-01-05',
                support_staff_id=user.id, 
                location='Lieu event', 
                number_of_participants=50, 
                notes='Notes event'
                )

            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "User not logged in. Please log in."
