import unittest
from unittest.mock import patch
from datetime import datetime

from UseCases.Remind.AddRemind import AddRemind, AddRemindArgs
from Model.Remind import Remind

class TestAddRemind(unittest.TestCase):

    @patch('UseCases.Remind.AddRemind.RemindRepository')
    def test_add_remind(self, mock_remind_repository):
        
        # Arrange
        repository = mock_remind_repository()
        add_remind = AddRemind(repository)
        args = AddRemindArgs(
            title='title',
            time=datetime(2024, 7, 3, 16, 52),
            user_id='2348778469543521',
            server_id='897894654321546',
            is_private=False
        )
        repository.get_channel_id_by_server_id.return_value = '987654321'
        repository.add.return_value = '123456789'

        # Act
        result = add_remind.execute(args)

        # Assert
        self.assertEqual(result, '123456789')
        repository.get_channel_id_by_server_id.assert_called_once_with('897894654321546')
        repository.add.assert_called_once_with('title', datetime(2024, 7, 3, 16, 52), '2348778469543521', '897894654321546', False)

    @patch('UseCases.Remind.AddRemind.RemindRepository')
    def test_add_remind_server_not_set_up(self, mock_remind_repository):
        
        # Arrange
        repository = mock_remind_repository()
        add_remind = AddRemind(repository)
        args = AddRemindArgs(
            title='title',
            time=datetime(2024, 7, 3, 16, 52),
            user_id='2348778469543521',
            server_id='897894654321546',
            is_private=False
        )
        repository.get_channel_id_by_server_id.return_value = None

        # Act
        with self.assertRaises(ValueError) as context:
            add_remind.execute(args)

        # Assert
        self.assertEqual(str(context.exception), 'Server is not set up for reminds')
        repository.get_channel_id_by_server_id.assert_called_once_with('897894654321546')

