import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import Client, User
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, Mock


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_delete_client_success(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a dummy user for the test (role: 'sales')
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Associate client with user
    client.sales_rep = user
    client.save()

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:

            call_command('delete_client', int(client.id))
            assert f"Client with ID {client.id} deleted successfully" in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_delete_client_not_sales_assigned(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
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
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('delete_client', int(client.id))
            except CommandError as ce:
                assert str(ce) == "Access denied. You are not the Sales Representative assigned to this client."


@pytest.mark.django_db
def test_delete_client_permission_failure(mocker, custom_input):
    # Create a dummy client for testing
    client = Client.objects.create(
        fullname='Client Test', 
        email='test@example.com'
        )

    # Create a dummy user for testing (role: 'support')
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
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='support')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('delete_client', int(client.id))
            except CommandError as ce:
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_client_client_not_found(mocker, custom_input):
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
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('delete_client', 999)
            except CommandError as ce:
                assert str(ce) == "Client with ID 999 not found"
