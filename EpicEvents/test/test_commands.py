from django.core.management.base import CommandError
from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from EpicEvents.management.commands.create_client import Command
from io import StringIO

User = get_user_model()

class CreateClientCommandTest(TestCase):

    def setUp(self):
        # Assuming 'admin' is the username with full permissions
        self.admin_user = User.objects.create_user('admin', password='Test123!')
        self.admin_user.save()
        self.client.login(username='admin', password='Test123!')
        self.inputs = {
            'Clients full name': 'Test Client',
            'Clients email': 'testclient@example.com',
            'Clients phone number': '1234567890',
            'Clients company name': 'Test Company'
        }
        self.out = StringIO()

    @patch('EpicEvents.management.commands.create_client.get_user_id_from_token')
    def test_get_user_id_from_token(self, mock_get_user_id_from_token):
        mock_get_user_id_from_token.return_value = self.admin_user.id
        self.assertEqual(self.admin_user.id, mock_get_user_id_from_token())




