import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import Contract, User, Client
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, Mock


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_delete_contract_success(mocker, custom_input):
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
        client=client, 
        sales_rep=sales, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy user for the test (role: 'management')
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='management'
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
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            call_command('delete_contract', int(contract.pk))

            # Checking the success message
            assert f"contract with ID {contract.pk} deleted sucessfully." in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_delete_contract_not_management_team(mocker, custom_input):
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
        client=client, 
        sales_rep=sales, 
        total_amount='1000.00',
        amount_remaining='800.00', 
        status='in progress'
        )

    # Create a dummy user for the test (role: 'sales')
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
                call_command('delete_contract', int(contract.pk))
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_contract_not_found(mocker, custom_input):
    # Create a dummy user for the test (role: 'management')
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='management'
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
                # Using an ID that doesn't exist
                call_command('delete_contract', 999)
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "contract with ID 999 does not exist"
