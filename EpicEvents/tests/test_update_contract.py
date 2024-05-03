from django.core.management import call_command
from django.core.management.base import CommandError
from epicevents.models import User, Client, Contract
from unittest.mock import patch, Mock
from datetime import datetime, timedelta, timezone
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_update_contract_successful(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="management"
    )

    sales = User.objects.create_user(
            username='comtest',
            fullname='sales Test', 
            role='sales'
        )

    client = Client.objects.create(
            fullname="CLient A", 
            email="clientA@gmail.com",
            phone="0606060606", 
            company_name="company A",
            sales_rep_id=sales.id
        )

    contract = Contract.objects.create(
            client_id=client.id,
            sales_rep_id=sales.id,
            total_amount=1000,
            amount_remaining=500,
            status='waiting for signature'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='management')

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=user)

    # Capturing standard output for verification
    call_command('update_contract', int(contract.id), '--status', 'signed')

    # Verifying that the contract was successfully modified
    user.refresh_from_db()
    captured = capsys.readouterr()
    assert f"contract with ID {contract.id} modified susseccfully." in captured.out


@pytest.mark.django_db
def test_update_user_permission_failure(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="support"
    )

    sales = User.objects.create_user(
            username='comtest',
            fullname='sales Test', 
            role='sales'
        )

    client = Client.objects.create(
            fullname="CLient A", 
            email="clientA@gmail.com",
            phone="0606060606", 
            company_name="company A",
            sales_rep_id=sales.id
        )

    contract = Contract.objects.create(
            client_id=client.id,
            sales_rep_id=sales.id,
            total_amount=1000,
            amount_remaining=500,
            status='waiting for signature',
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='support')

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Creating an instance of the command
            try:
                # Capturing standard output for verification
                call_command('update_contract', int(contract.id), '--status', 'signed')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_contract_not_found(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="management"
    )

    sales = User.objects.create_user(
            username='comtest',
            fullname='sales Test', 
            role='sales'
        )

    client = Client.objects.create(
        fullname="CLient A", 
        email="clientA@gmail.com",
        phone="0606060606", 
        company_name="company A",
        sales_rep_id=sales.id
        )

    # ID of a user that does not exist
    contract_id = 999

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='management')

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=user)

        # Capturing standard error output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Attempting to update a user that does not exist
            try:
                call_command('update_contract', int(contract_id), '--status', 'signed')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == f"Contract with ID {contract_id} does not exist."


@pytest.mark.django_db
def test_update_contract_not_authenticated(mocker, capsys):
    sales = User.objects.create_user(
        username='comtest',
        fullname='sales Test', 
        role='sales'
        )

    client = Client.objects.create(
        fullname="CLient A", 
        email="clientA@gmail.com",
        phone="0606060606", 
        company_name="company_name A",
        sales_rep_id=sales.id
        )

    contract = Contract.objects.create(
        client_id=client.id,
        sales_rep_id=sales.id,
        total_amount=1000,
        amount_remaining=500,
        status='waiting for signature'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='management')

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=(None, None))

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Creating an instance of the command
            try:
                # Capturing standard output for verification
                call_command('update_contract', int(contract.id), '--status', 'signed')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "User not logged in. Please log in."
