import unittest
from unittest.mock import patch
from datetime import datetime

from UseCases.Remind.RemoveRemind import RemoveRemind
from Model.Remind import Remind

class TestRemoveRemind(unittest.TestCase):
    
        @patch('UseCases.Remind.RemoveRemind.RemindRepository')
        def test_remove_remind_normal(self, mock_remind_repository):
            
            # Arrange
            repository = mock_remind_repository()
            remove_remind = RemoveRemind(repository)
            remind_id = '123456789'
            server_id = '897894654321546'
            user_id = '2348778469543521'
            repository.get_reminds_by_user_id.return_value = [
                Remind(
                    id=remind_id,
                    title='title',
                    time=datetime(2024, 7, 3, 16, 52),
                    user_id=user_id,
                    server_id=server_id,
                    is_private=False
                )
            ]

            # Act
            remove_remind.execute(remind_id, server_id, user_id)

            # Assert
            repository.remove.assert_called_once_with(remind_id)

        @patch('UseCases.Remind.RemoveRemind.RemindRepository')
        def test_remove_remind_from_different_user_and_same_server(self, mock_remind_repository):
            
            # Arrange
            repository = mock_remind_repository()
            remove_remind = RemoveRemind(repository)
            remind_id = '123456789'
            server_id = '897894654321546'
            user_id = '2348778469543521'
            repository.get_reminds_by_user_id.return_value = [
                Remind(
                    id=remind_id,
                    title='title',
                    time=datetime(2024, 7, 3, 16, 52),
                    user_id='024681012141618',
                    server_id=server_id,
                    is_private=False
                )
            ]

            # Act
            with self.assertRaises(ValueError) as context:
                remove_remind.execute(remind_id, server_id, user_id)

            # Assert
            self.assertEqual(str(context.exception), 'Remind not found')

        @patch('UseCases.Remind.RemoveRemind.RemindRepository')
        def test_remove_remind_from_same_user_and_different_server(self, mock_remind_repository):
            
            # Arrange
            repository = mock_remind_repository()
            remove_remind = RemoveRemind(repository)
            remind_id = '123456789'
            server_id = '897894654321546'
            user_id = '2348778469543521'
            repository.get_reminds_by_user_id.return_value = [
                Remind(
                    id=remind_id,
                    title='title',
                    time=datetime(2024, 7, 3, 16, 52),
                    user_id=user_id,
                    server_id='987654321',
                    is_private=False
                )
            ]

            # Act
            with self.assertRaises(ValueError) as context:
                remove_remind.execute(remind_id, server_id, user_id)

            # Assert
            self.assertEqual(str(context.exception), 'Remind not found')

        @patch('UseCases.Remind.RemoveRemind.RemindRepository')
        def test_remove_remind_from_different_user_and_different_server(self, mock_remind_repository):
                
                # Arrange
                repository = mock_remind_repository()
                remove_remind = RemoveRemind(repository)
                remind_id = '123456789'
                server_id = '897894654321546'
                user_id = '2348778469543521'
                repository.get_reminds_by_user_id.return_value = [
                    Remind(
                        id=remind_id,
                        title='title',
                        time=datetime(2024, 7, 3, 16, 52),
                        user_id='024681012141618',
                        server_id='987654321',
                        is_private=False
                    )
                ]
    
                # Act
                with self.assertRaises(ValueError) as context:
                    remove_remind.execute(remind_id, server_id, user_id)
    
                # Assert
                self.assertEqual(str(context.exception), 'Remind not found')

        @patch('UseCases.Remind.RemoveRemind.RemindRepository')
        def test_remove_remind_remind_not_found(self, mock_remind_repository):
            
            # Arrange
            repository = mock_remind_repository()
            remove_remind = RemoveRemind(repository)
            remind_id = '123456789'
            server_id = '897894654321546'
            user_id = '2348778469543521'
            repository.get_reminds_by_user_id.return_value = []

            # Act
            with self.assertRaises(ValueError) as context:
                remove_remind.execute(remind_id, server_id, user_id)

            # Assert
            self.assertEqual(str(context.exception), 'Remind not found')
