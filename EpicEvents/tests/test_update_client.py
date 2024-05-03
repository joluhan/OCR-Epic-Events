from django.core.management import call_command
from django.core.management.base import CommandError
from epicevents.models import User, Client
from unittest.mock import patch, Mock
from datetime import datetime, timedelta, timezone
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_update_client_successful(mocker, capsys):
    # Create a dummy user for testing
    sales = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="sales"
    )

    client = Client.objects.create(
            fullname="test client", 
            email="testmail@gmail.com",
            phone="0909090909", 
            company_name="company test",
            sales_rep_id=sales.id
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('epicevents.permissions.get_user_id_from_token', return_value=sales.id)

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=sales)

    # Capturing standard output for verification
    call_command('update_client', int(client.id), fullname='New Name')

    # Verifying that the client was successfully modified
    sales.refresh_from_db()
    captured = capsys.readouterr()
    assert f"Client with ID {client.id} modified successfully." in captured.out


@pytest.mark.django_db
def test_update_client_permission_failure(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="support"
    )

    client = Client.objects.create(
            fullname="test client", 
            email="testmail@gmail.com",
            phone="0909090909", 
            company_name="company test",
            sales_rep_id=user.id
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
                call_command('update_client', int(client.id), fullname='New Name')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_client_not_authenticated(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="management"
    )

    client = Client.objects.create(
            fullname="test client", 
            email="testmail@gmail.com",
            phone="0909090909", 
            company_name="company test",
            sales_rep_id=user.id
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.load_token', return_value=(None, None))

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Creating an instance of the command
            try:
                # Capturing standard output for verification
                call_command('update_client', int(client.id), '--fullname', 'New Name')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "User not logged in. Please log in."
