import pytest
from django.core.management import call_command
from epicevents.models import User
from epicevents.management.commands.create_client import Command
from unittest.mock import patch, Mock
from datetime import datetime, timedelta, timezone
from django.core.management.base import CommandError


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_create_client_success(mocker, custom_input):
    # Dummy user for testing
    user = User.objects.create_user(
            username='testuser', 
            password='testpassword',
            fullname='Test User', 
            role='sales'
        )

    # Expected output data for the test
    expected_output = "'Test Client' created successfully"

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):

        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('epicevents.permissions.get_user_id_from_token', return_value=user.id)

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        mocker.patch('epicevents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            cmd = Command()

            # Calling the command handle function
            cmd.handle(
                fullname='Test Client',
                email='testclient@example.com',
                phone='123456789',
                company_name='Test Company',
            )

            # Checking standard output
            assert expected_output in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_create_client_permission_failure(mocker, custom_input):
    # Creating a dummy user for testing with the appropriate role
    user = User.objects.create_user(
                username='testuser',
                password='testpassword',
                fullname='Test User',
                role='management'
            )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Mock user creation in database
    mocker.patch('epicevents.models.User.objects.create_user', return_value=user)

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock to bypass permission check
        mocker.patch('epicevents.permissions.get_user_role_from_token', return_value='management')

        # Mock the load_token function to return a valid token
        mocker.patch('epicevents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))

        # Mock the validate_token function to return a valid user
        # mocker.patch('epicevents.auth_utils.validate_token', return_value=User.objects.create_user(username='testuser', role='management'))
        mocker.patch('epicevents.permissions.validate_token', return_value=user)

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            cmd = Command()

            # Calling the command handle function
            with pytest.raises(CommandError) as exc_info:
                cmd.handle(
                    fullname='Test User', 
                    company_name='Test Compnay', 
                    username='testuser', 
                    email='testuser@example.com'
                )

            # Checking the error message
            assert str(exc_info.value) == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_create_client_not_connected(mocker, custom_input):
    # Dummy user for testing
    user = User.objects.create_user(
                username='testuser',
                password='testpassword',
                fullname='Test User',
                role='management'
            )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Mock user creation in database
    mocker.patch('epicevents.models.User.objects.create_user', return_value=user)

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        # Mock load_token function to return None (user not logged in)
        mocker.patch('epicevents.permissions.load_token', return_value=(None, None))

        # Capturing standard output for verification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Creating an instance of the command
            cmd = Command()

            # Calling the command handle function without logged in user
            with pytest.raises(CommandError) as exc_info:
                cmd.handle(
                    fullname='Test User', 
                    company_name='Test Compnay', 
                    username='testuser', 
                    email='testuser@example.com'
                )

            # Checking the error message
            assert str(exc_info.value) == "User not logged in. Please log in."
