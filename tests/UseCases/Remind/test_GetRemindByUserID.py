import unittest
from unittest.mock import patch
from datetime import datetime

from UseCases.Remind.GetRemindByUserID import GetRemindByUserID
from Model.Remind import Remind

class TestGetRemindByUserID(unittest.TestCase):

    @patch('UseCases.Remind.GetRemindByUserID.RemindRepository')
    def test_get_remind_by_user_id(self, mock_remind_repository):
        
        # Arrange
        repository = mock_remind_repository()
        get_remind_by_user_id = GetRemindByUserID(repository)
        remind = Remind(
            id='123456789',
            title='title',
            time=datetime(2024, 7, 3, 16, 52),
            user_id='2348778469543521',
            server_id='897894654321546',
            is_private=False
        )
        repository.get_reminds_by_user_id.return_value = [remind]

        # Act
        result = get_remind_by_user_id.execute('2348778469543521')

        # Assert
        self.assertEqual(result, [remind])
        repository.get_reminds_by_user_id.assert_called_once_with('2348778469543521')

    @patch('UseCases.Remind.GetRemindByUserID.RemindRepository')
    def test_get_remind_by_user_id_no_reminds(self, mock_remind_repository):
        
        # Arrange
        repository = mock_remind_repository()
        get_remind_by_user_id = GetRemindByUserID(repository)
        repository.get_reminds_by_user_id.return_value = []

        # Act
        result = get_remind_by_user_id.execute('2348778469543521')

        # Assert
        self.assertEqual(result, [])
        repository.get_reminds_by_user_id.assert_called_once_with('2348778469543521')