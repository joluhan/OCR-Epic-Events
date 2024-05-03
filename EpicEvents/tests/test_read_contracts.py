import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import User, Contract, Client
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from io import StringIO
import sys


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_read_contracts_connected_user(mocker):
    # Create a dummy user for testing
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='support'
        )

    sales_a = User.objects.create_user(
        username='commerA',
        fullname='sales A', 
        role='sales'
        )

    sales_b = User.objects.create_user(
        username='commerB',
        fullname='sales B', 
        role='sales'
        )

    client_a = Client.objects.create(
        fullname="CLient A", 
        email="clientA@gmail.com",
        phone="0606060606", 
        company_name="company_name A",
        sales_rep=sales_a
        )
    
    client_b = Client.objects.create(
        fullname="CLient B", 
        email="clientB@gmail.com",
        phone="0707070707", 
        company_name="company_name B",
        sales_rep=sales_b
        )

    contract1 = Contract.objects.create(
        client=client_a,
        sales_rep=sales_a,
        total_amount=1000,
        amount_remaining=500,
        status='waiting for signature'
        )

    contract2 = Contract.objects.create(
        client=client_b,
        sales_rep=sales_b,
        total_amount=5000,
        amount_remaining=2000,
        status='signed'
        )
    
    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='support')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output = "List of Contracts\n"
        
        original_stdout = StringIO()
        sys.stdout = original_stdout

        call_command('read_contracts')
        captured_output = original_stdout.getvalue().strip()

        sys.stdout = sys.__stdout__

        assert expected_output.strip() in captured_output.strip()


@pytest.mark.django_db
def test_read_contracts_with_filters(mocker):
    # Create a dummy user for testing
    user = User.objects.create_user(
        username='testuser', 
        password='testpassword',
        fullname='Test User', 
        role='sales'
        )

    # Create mock clients for testing
    client_a = Client.objects.create(
        fullname="Client A", 
        email="clientA@gmail.com",
        phone="0606060606", 
        company_name="company_name A",
        sales_rep=user
        )

    client_b = Client.objects.create(
        fullname="Client B", 
        email="clientB@gmail.com",
        phone="0707070707", 
        company_name="company_name B",
        sales_rep=user
        )

    # Create dummy contracts for testing
    contract1 = Contract.objects.create(
        client=client_a,
        sales_rep=user,
        total_amount=1000,
        amount_remaining=500,
        status='waiting for signature'
        )

    contract2 = Contract.objects.create(
        client=client_b,
        sales_rep=user,
        total_amount=5000,
        amount_remaining=2000,
        status='signed'
        )

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output1 = "List of Contracts\n"
        expected_output2 = "List of Contracts\n"

        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        call_command('read_contracts', '--client', 'Client A')
        captured_output1 = sys.stdout.getvalue().strip()

        call_command('read_contracts', '--total_amount', '5000')
        captured_output2 = sys.stdout.getvalue().strip()

        sys.stdout = original_stdout

        assert expected_output1.strip() in captured_output1.strip()
        assert "Client A" in captured_output1

        assert expected_output2.strip() in captured_output2.strip()
        assert "Client B" in captured_output2
        assert "5000" in captured_output2


@pytest.mark.django_db
def test_read_contracts_unauthenticated_user(mocker):
    # Create a fictitious user who is not logged in
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
            call_command('read_contracts')
        except CommandError as e:
            assert str(e) == expected_output
