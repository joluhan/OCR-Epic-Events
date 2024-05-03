import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from EpicEvents.models import Event, Contract, User, Client
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from io import StringIO
import sys


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_read_events_connected_user(mocker):
    # Create a dummy user for testing
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    fullname='Test User', role='sales')
    sales_a = User.objects.create_user(username='commerA',
                                            fullname='sales A', role='sales')

    sales_b = User.objects.create_user(username='commerB',
                                            fullname='sales B', role='sales')

    client_a = Client.objects.create(fullname="CLient A", email="clientA@gmail.com",
                                     phone="0606060606", company_name="company_name A",
                                     sales_rep=sales_a)

    client_b = Client.objects.create(fullname="CLient B", email="clientB@gmail.com",
                                     phone="0707070707", company_name="company_name B",
                                     sales_rep=sales_b)

    support_a = User.objects.create_user(username='suppA',
                                         fullname='Support A', role='support')

    support_b = User.objects.create_user(username='suppB',
                                         fullname='Support B', role='support')
    
    # Create dummy contracts for testing
    contract1 = Contract.objects.create(client=client_a,
                                      sales_rep=user,
                                      total_amount=1000,
                                      amount_remaining=500,
                                      status='waiting for signature'
                                      )

    contract2 = Contract.objects.create(client=client_b,
                                      sales_rep=user,
                                      total_amount=5000,
                                      amount_remaining=2000,
                                      status='signed'
                                      )
    
    # Create dummy events for the test
    event1 = Event.objects.create(contract=contract1,
                                          name="event A",
                                          start_date=datetime(2023, 12, 15),
                                          end_date=datetime(2023, 12, 16),
                                          support_staff=support_a,
                                          location="location A",
                                          attendees=50,
                                          notes="Notes A")

    event2 = Event.objects.create(contract=contract2,
                                          name="event B",
                                          start_date=datetime(2023, 12, 20),
                                          end_date=datetime(2023, 12, 22),
                                          support_staff=support_b,
                                          location="location B",
                                          attendees=150,
                                          notes="Notes B")

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='support')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output = "List of Events\n"
        original_stdout = StringIO()
        sys.stdout = original_stdout

        call_command('read_events')
        captured_output = original_stdout.getvalue().strip()

        sys.stdout = sys.__stdout__

        assert expected_output.strip() in captured_output.strip()
        assert event1.name in captured_output
        assert event2.name in captured_output


@pytest.mark.django_db
def test_read_events_with_filters(mocker):
    # Create a dummy user for testing
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    fullname='Test User', role='sales')
    sales_a = User.objects.create_user(username='commerA',
                                            fullname='sales A', role='sales')

    sales_b = User.objects.create_user(username='commerB',
                                            fullname='sales B', role='sales')

    client_a = Client.objects.create(fullname="CLient A", email="clientA@gmail.com",
                                     phone="0606060606", company_name="company_name A",
                                     sales_rep=sales_a)

    client_b = Client.objects.create(fullname="CLient B", email="clientB@gmail.com",
                                     phone="0707070707", company_name="company_name B",
                                     sales_rep=sales_b)

    support_a = User.objects.create_user(username='suppA',
                                         fullname='Support A', role='support')

    support_b = User.objects.create_user(username='suppB',
                                         fullname='Support B', role='support')
    
    # Create dummy contracts for testing
    contract1 = Contract.objects.create(client=client_a,
                                      sales_rep=user,
                                      total_amount=1000,
                                      amount_remaining=500,
                                      status='waiting for signature'
                                      )

    contract2 = Contract.objects.create(client=client_b,
                                      sales_rep=user,
                                      total_amount=5000,
                                      amount_remaining=2000,
                                      status='signed'
                                      )

    # Create dummy events for the test
    event1 = Event.objects.create(contract=contract1,
                                          name="event A",
                                          start_date=datetime(2023, 12, 15),
                                          end_date=datetime(2023, 12, 16),
                                          support_staff=support_a,
                                          location="location A",
                                          attendees=50,
                                          notes="Notes A")

    event2 = Event.objects.create(contract=contract2,
                                          name="event B",
                                          start_date=datetime(2023, 12, 20),
                                          end_date=datetime(2023, 12, 22),
                                          support_staff=support_b,
                                          location="location B",
                                          attendees=150,
                                          notes="Notes B")

    # Mock the getpass function to avoid real password requests
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value='sales')
        mocker.patch('EpicEvents.permissions.load_token', return_value=('test_token', datetime.now(timezone.utc) + timedelta(days=1)))
        mocker.patch('EpicEvents.permissions.validate_token', return_value=user)

        expected_output1 = "List of Events\n"
        expected_output2 = "List of Events\n"

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        call_command('read_events', '--name', 'event A')
        captured_output1 = sys.stdout.getvalue().strip()

        call_command('read_events', '--location', 'location B')
        captured_output2 = sys.stdout.getvalue().strip()
        sys.stdout = original_stdout

        assert expected_output1.strip() in captured_output1.strip()
        assert "event A" in captured_output1
        # assert "Support A" in captured_output1

        assert expected_output2.strip() in captured_output2.strip()
        assert "event B" in captured_output2
        # assert "Support B" in captured_output2


@pytest.mark.django_db
def test_read_events_unauthenticated_user(mocker):
    user = User.objects.create_user(username='unauthenticated_user', password='testpassword')
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Using patch to simulate user input
    with patch('builtins.input', side_effect=custom_input):
        mocker.patch('EpicEvents.permissions.get_user_role_from_token', return_value=None)
        mocker.patch('EpicEvents.permissions.load_token', return_value=(None, None))

        expected_output = "User not logged in. Please log in."

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            call_command('read_events')
        except CommandError as e:
            assert str(e) == expected_output
