import pytest
from django.core.management import call_command
from EpicEvents.models import Client, User
from django.core.management.base import CommandError
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from io import StringIO
import sys


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_read_clients_all_info_connected(mocker):
    # Dummy user for testing
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Create mock clients for testing
    client1 = Client.objects.create(
        fullname='Client A',
        email='client_a@example.com', 
        phone='123456789', 
        company_name='company_name A'
        )
    
    client2 = Client.objects.create(
        fullname='Client B',
        email='client_b@example.com', 
        phone='987654321', 
        company_name='company_name B'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output = "List of Clients\n"

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        call_command('read_clients')
        captured_output = sys.stdout.getvalue().strip()

        sys.stdout = original_stdout

        assert expected_output.strip() in captured_output.strip()


@pytest.mark.django_db
def test_read_clients_with_details(mocker):
    # Dummy user for testing
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Create mock clients for testing
    client1 = Client.objects.create(
        fullname='Client A', 
        email='client_a@example.com',
        phone='123456789', 
        company_name='company_name A'
        )
    
    client2 = Client.objects.create(
        fullname='Client B', 
        email='client_b@example.com',
        phone='987654321', 
        company_name='company_name B'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output1 = "List of Clients\n"
        expected_output2 = "List of Clients\n"

        # Rediriger la sortie standard
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        call_command('read_clients', '--fullname', 'Client A')
        captured_output1 = sys.stdout.getvalue().strip()

        call_command('read_clients', '--email', 'client_b@example.com')
        captured_output2 = sys.stdout.getvalue().strip()

        sys.stdout = original_stdout

        assert expected_output1.strip() in captured_output1.strip()
        assert expected_output2.strip() in captured_output2.strip()


@pytest.mark.django_db
def test_read_clients_unauthenticated_user(mocker):
    user = User.objects.create_user(username='unauthenticated_user', password='testpassword')

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value=None)
        mocker.patch('EpicEvents.permissions.load_token', return_value=(None, None))

        expected_output = "User not logged in. Please log in."

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            call_command('read_clients', '--fullname', 'Client A')
        except CommandError as e:
            assert str(e) == expected_output
