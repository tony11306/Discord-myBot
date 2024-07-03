import unittest
from unittest.mock import patch
from datetime import datetime

from UseCases.Remind.UnbindRemindChannel import UnbindRemindChannel

class TestUnbindRemindChannel(unittest.TestCase):

    @patch('UseCases.Remind.UnbindRemindChannel.RemindRepository')
    def test_unbind_remind_channel(self, mock_remind_repository):
        
        # Arrange
        repository = mock_remind_repository()
        unbind_remind_channel = UnbindRemindChannel(repository)
        server_id = '897894654321546'
        repository.get_channel_id_by_server_id.return_value = '987654321'

        # Act
        unbind_remind_channel.execute(server_id)

        # Assert
        repository.get_channel_id_by_server_id.assert_called_once_with(server_id)
        repository.remove_remind_channel.assert_called_once_with(server_id)

    @patch('UseCases.Remind.UnbindRemindChannel.RemindRepository')
    def test_unbind_remind_channel_with_no_channel_binded(self, mock_remind_repository):
            
            # Arrange
            repository = mock_remind_repository()
            unbind_remind_channel = UnbindRemindChannel(repository)
            server_id = '897894654321546'
            repository.get_channel_id_by_server_id.return_value = None
    
            # Act
            with self.assertRaises(ValueError) as context:
                unbind_remind_channel.execute(server_id)
    
            # Assert
            repository.get_channel_id_by_server_id.assert_called_once_with(server_id)
            self.assertEqual(str(context.exception), 'Server is not set up for reminds')
            repository.remove_remind_channel.assert_not_called()