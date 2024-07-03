import unittest
from unittest.mock import patch
from datetime import datetime

from UseCases.Remind.BindRemindChannel import BindRemindChannel
from Model.Remind import Remind

class TestBindRemindChannel(unittest.TestCase):

    @patch('UseCases.Remind.BindRemindChannel.RemindRepository')
    def test_bind_remind_channel(self, mock_remind_repository):
        
        # Arrange
        repository = mock_remind_repository()
        bind_remind_channel = BindRemindChannel(repository)
        remind = Remind(
            id='123456789',
            title='title',
            time=datetime(2024, 7, 3, 16, 52),
            user_id='2348778469543521',
            server_id='897894654321546',
            is_private=False
        )
        channel_id = '987654321'
        repository.get_channel_id_by_server_id.return_value = None

        # Act
        bind_remind_channel.execute(remind.server_id, channel_id)

        # Assert
        repository.get_channel_id_by_server_id.assert_called_once_with(remind.server_id)
        repository.add_remind_channel.assert_called_once_with(remind.server_id, channel_id)

    @patch('UseCases.Remind.BindRemindChannel.RemindRepository')
    def test_bind_remind_channel_with_channel_already_binded(self, mock_remind_repository):
            
            # Arrange
            repository = mock_remind_repository()
            bind_remind_channel = BindRemindChannel(repository)
            remind = Remind(
                id='123456789',
                title='title',
                time=datetime(2024, 7, 3, 16, 52),
                user_id='2348778469543521',
                server_id='897894654321546',
                is_private=False
            )
            channel_id = '987654321'
            repository.get_channel_id_by_server_id.return_value = channel_id
    
            # Act
            with self.assertRaises(ValueError) as context:
                bind_remind_channel.execute(remind.server_id, channel_id)
    
            # Assert
            repository.get_channel_id_by_server_id.assert_called_once_with(remind.server_id)
            self.assertEqual(str(context.exception), 'Server is already set up for reminds')
            repository.add_remind_channel.assert_not_called()