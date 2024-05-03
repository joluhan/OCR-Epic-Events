import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import User
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from io import StringIO
import sys


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_read_users_connected_user(mocker):
    # Create a dummy user for testing
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
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='admin')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output = "List of users\n"

        original_stdout = StringIO()
        sys.stdout = original_stdout

        call_command('read_users')
        captured_output = original_stdout.getvalue().strip()

        sys.stdout = sys.__stdout__

        assert expected_output.strip() in captured_output.strip()


@pytest.mark.django_db
def test_read_users_with_filters(mocker):
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )


    user1 = User.objects.create(
        fullname='user A', 
        role='support',
        username='collabA'
        )
    
    user2 = User.objects.create(
        fullname='user B', 
        role='sales',
        username='collabB'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output1 = "List of users\n"
        expected_output2 = "List of users\n"

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        call_command('read_users', '--fullname', 'user A')
        captured_output1 = sys.stdout.getvalue().strip()

        call_command('read_users', '--username', 'collabB')
        captured_output2 = sys.stdout.getvalue().strip()

        sys.stdout = original_stdout

        assert expected_output1.strip() in captured_output1.strip()
        assert "user A" in captured_output1
        assert "support" in captured_output1

        assert expected_output2.strip() in captured_output2.strip()
        assert "user B" in captured_output2
        assert "sales" in captured_output2


@pytest.mark.django_db
def test_read_users_unauthenticated_user(mocker):
    user = User.objects.create_user(
        username='unauthenticated_user', 
        password='testpassword'
        )

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
            call_command('read_users')
        except CommandError as e:
            assert str(e) == expected_output
