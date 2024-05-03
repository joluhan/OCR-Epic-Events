from django.test import TestCase
from django.core.management.base import CommandError
from unittest.mock import patch, MagicMock
from EpicEvents.permissions import require_login, is_management_team, is_sales_team, is_sales_team_and_client_rep
from EpicEvents.permissions import is_contract_sales_rep_or_is_management_team, require_sales_event_access, is_event_support_or_is_management_team

class RequireLoginTestCase(TestCase):
    @patch('EpicEvents.permissions.load_token')
    @patch('EpicEvents.permissions.validate_token')
    def test_require_login_with_valid_token(self, mock_validate_token, mock_load_token):
        # Arrange
        mock_load_token.return_value = ['valid_token']
        mock_validate_token.return_value = MagicMock()
        
        # Act & Assert
        @require_login
        def dummy_command(*args, **kwargs):
            return True
        
        self.assertTrue(dummy_command())

    @patch('EpicEvents.permissions.load_token')
    @patch('EpicEvents.permissions.validate_token')
    def test_require_login_with_no_token(self, mock_validate_token, mock_load_token):
        # Arrange
        mock_load_token.return_value = [None]
        mock_validate_token.return_value = None
        
        # Act & Assert
        @require_login
        def dummy_command(*args, **kwargs):
            return True
        
        with self.assertRaises(CommandError) as cm:
            dummy_command()
        
        self.assertEqual("User not logged in. Please log in.", str(cm.exception))

    @patch('EpicEvents.permissions.load_token')
    @patch('EpicEvents.permissions.validate_token')
    def test_require_login_with_invalid_token(self, mock_validate_token, mock_load_token):
        # Arrange
        mock_load_token.return_value = ['invalid_token']
        mock_validate_token.return_value = None
        
        # Act & Assert
        @require_login
        def dummy_command(*args, **kwargs):
            return True
        
        with self.assertRaises(CommandError) as cm:
            dummy_command()
        
        self.assertEqual("Invalid token. Please log in.", str(cm.exception))

class IsManagementTeamTestCase(TestCase):
    @patch('EpicEvents.permissions.get_user_role_from_token')
    def test_is_management_team_with_correct_role(self, mock_get_user_role_from_token):
        # Arrange
        mock_get_user_role_from_token.return_value = "management"
        request = MagicMock()

        # Act & Assert
        @is_management_team
        def dummy_view(request):
            return True
        
        self.assertTrue(dummy_view(request))

    @patch('EpicEvents.permissions.get_user_role_from_token')
    def test_is_management_team_with_incorrect_role(self, mock_get_user_role_from_token):
        # Arrange
        mock_get_user_role_from_token.return_value = "not_management"
        request = MagicMock()

        # Act & Assert
        @is_management_team
        def dummy_view(request):
            return True
        
        with self.assertRaises(CommandError):
            dummy_view(request)

class IsSalesTeamTestCase(TestCase):
    @patch('EpicEvents.permissions.get_user_role_from_token')
    def test_is_sales_team_with_correct_role(self, mock_get_user_role_from_token):
        mock_get_user_role_from_token.return_value = "sales"
        request = MagicMock()

        @is_sales_team
        def dummy_view(request):
            return True
        
        self.assertTrue(dummy_view(request))

    @patch('EpicEvents.permissions.get_user_role_from_token')
    def test_is_sales_team_with_incorrect_role(self, mock_get_user_role_from_token):
        mock_get_user_role_from_token.return_value = "not_sales"
        request = MagicMock()

        @is_sales_team
        def dummy_view(request):
            return True
        
        with self.assertRaises(CommandError):
            dummy_view(request)

class IsSalesTeamAndClientRepTestCase(TestCase):
    @patch('EpicEvents.permissions.get_user_role_from_token')
    @patch('EpicEvents.permissions.get_user_id_from_token')
    @patch('EpicEvents.models.Client.objects.get')
    def test_is_sales_team_and_client_rep_with_correct_role_and_client(self, mock_client_get, mock_get_user_id_from_token, mock_get_user_role_from_token):
        mock_get_user_role_from_token.return_value = "sales"
        mock_get_user_id_from_token.return_value = 'user_id'
        mock_client_get.return_value = MagicMock()
        request = MagicMock()
        kwargs = {'client_id': 'client_id'}

        @is_sales_team_and_client_rep
        def dummy_view(request, **kwargs):
            return True
        
        self.assertTrue(dummy_view(request, **kwargs))

class IsContractSalesRepOrIsManagementTeamTestCase(TestCase):
    @patch('EpicEvents.permissions.get_user_role_from_token')
    @patch('EpicEvents.permissions.get_user_id_from_token')
    @patch('EpicEvents.models.Contract.objects.get')
    def test_with_sales_role_and_correct_contract(self, mock_contract_get, mock_get_user_id_from_token, mock_get_user_role_from_token):
        # Arrange
        mock_get_user_role_from_token.return_value = "sales"
        mock_get_user_id_from_token.return_value = 'user_id'
        mock_contract_get.return_value = MagicMock()
        request = MagicMock()
        kwargs = {'contract_id': 'contract_id'}

        # Act & Assert
        @is_contract_sales_rep_or_is_management_team
        def dummy_view(request, **kwargs):
            return True
        
        self.assertTrue(dummy_view(request, **kwargs))

class RequireSalesEventAccessTestCase(TestCase):
    @patch('EpicEvents.permissions.get_user_role_from_token')
    @patch('EpicEvents.permissions.get_user_id_from_token')
    @patch('EpicEvents.models.Contract.objects.get')
    def test_with_sales_role_linked_to_contract_customer(self, mock_contract_get, mock_get_user_id_from_token, mock_get_user_role_from_token):
        # Arrange
        mock_get_user_role_from_token.return_value = "sales"
        mock_get_user_id_from_token.return_value = 'user_id'
        mock_contract_get.return_value = MagicMock()
        request = MagicMock()
        kwargs = {'contract_id': 'contract_id'}

        # Act & Assert
        @require_sales_event_access
        def dummy_view(request, **kwargs):
            return True
        
        self.assertTrue(dummy_view(request, **kwargs))

class IsEventSupportOrIsManagementTeamTestCase(TestCase):
    @patch('EpicEvents.permissions.get_user_role_from_token')
    @patch('EpicEvents.permissions.get_user_id_from_token')
    @patch('EpicEvents.models.Event.objects.get')
    def test_with_support_role_and_assigned_to_event(self, mock_event_get, mock_get_user_id_from_token, mock_get_user_role_from_token):
        # Arrange
        mock_get_user_role_from_token.return_value = "support"
        mock_get_user_id_from_token.return_value = 'user_id'
        mock_event_get.return_value = MagicMock()
        request = MagicMock()
        kwargs = {'event_id': 'event_id'}

        # Act & Assert
        @is_event_support_or_is_management_team
        def dummy_view(request, **kwargs):
            return True
        
        self.assertTrue(dummy_view(request, **kwargs))


