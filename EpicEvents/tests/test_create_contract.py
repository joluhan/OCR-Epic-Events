import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.management.commands.create_contract import Command
from EpicEvents.models import User, Client
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, Mock


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_create_contract_success(mocker, custom_input):
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

    expected_output = "Contract 1 created sucessfully."

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Mock user creation in database
    mocker.patch('EpicEvents.models.User.objects.create_user', return_value=sales)

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='management')

        # Mock the load_token function to return a valid token
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('EpicEvents.permissions.validate_token', return_value=sales)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            call_command(
                'create_contract', 
                client_id=int(client.id), 
                sales_rep_id=int(sales.id), 
                total_amount='1000.00', 
                amount_remaining='800.00', 
                status='in progress'
            )

            # Checking the success message
            assert expected_output in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_create_contract_permission_failure(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
            fullname='Client Test', 
            email='test@example.com'
        )

    # Create a dummy user for the test (role: 'sales' rather than 'manager')
    user = User.objects.create_user(
            username='testuser', 
            password='testpassword',
            fullname='Test User', 
            role='sales'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Mock user creation in database
    mocker.patch('EpicEvents.models.User.objects.create_user', return_value=user)

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')

        # Mock the load_token function to return a valid token
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            cmd = Command()

            # Calling the command handle function with the correct arguments
            try:
                cmd.handle(
                    client_id=str(client.id), 
                    sales_rep_id=str(user.id), 
                    total_amount='1000.00',
                    amount_remaining='800.00', 
                    status='in progress'
                )

            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_create_contract_unauthenticated_user(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
            fullname='Client Test', 
            email='test@example.com'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check (utilisateur non connecté)
        mocker.patch('EpicEvents.permissions.load_token', return_value=(None, None))

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            cmd = Command()

            # Calling the command handle function with the correct arguments
            try:
                cmd.handle(
                    client_id=str(client.id), 
                    sales_rep_id='1', 
                    total_amount='1000.00',
                    amount_remaining='800.00',
                    status='in progress'
                )

            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "User not logged in. Please log in."
