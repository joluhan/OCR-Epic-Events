from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import User
from unittest.mock import patch, Mock
from datetime import datetime, timedelta, timezone
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_update_user_successful(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="management"
    )

    mocker.patch('getpass.getpass', return_value='testpassword')

    with patch('builtins.input', side_effect=custom_input):

        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='management')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

    call_command('update_user', int(user.id), '--fullname', 'New Name')

    # Verifying that the user was successfully modified
    user.refresh_from_db()
    captured = capsys.readouterr()
    assert f"user with ID {user.id} modified successfully" in captured.out


@pytest.mark.django_db
def test_update_user_permission_failure(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="sales"
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
                call_command('update_user', int(user.id), '--fullname', 'New Name')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_user_not_found(mocker, capsys):
    user = User.objects.create_user(
            username='testuser', 
            password='testpassword', 
            fullname='Test User', 
            role='management'
        )

    # ID of a user that does not exist
    user_id = 999

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='management')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Attempting to update a user that does not exist
            try:
                call_command('update_user', int(user_id), '--fullname', 'New Name')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == f"user with ID {user_id} not found"


@pytest.mark.django_db
def test_update_user_not_authenticated(mocker, capsys):
    # Create a dummy user for testing
    user = User.objects.create(
        fullname="user Test",
        username="testuser",
        password="testpassword",
        role="management"
    )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.load_token', return_value=(None, None))

        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            try:
                call_command('update_user', int(user.id), '--fullname', 'New Name')
            except CommandError as ce:
                # Checking the error message
                assert str(ce) == "User not logged in. Please log in."
