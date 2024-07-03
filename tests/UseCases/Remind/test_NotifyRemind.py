import unittest
from unittest.mock import patch, AsyncMock
from datetime import datetime
import asyncio
from freezegun import freeze_time

from Model.Remind import Remind
from UseCases.Remind.NotifyRemind import NotifyRemind, NotifyRemindOutputPort

class TestNotifyRemind(unittest.TestCase):

    def setUp(self) -> None:
        self.reminds = [
            Remind(
                id='123456789',
                title='title',
                time=datetime(2024, 7, 3, 16, 52),
                user_id='2348778469543521',
                server_id='897894654321546',
                is_private=False
            ),
            Remind(
                id='987654321',
                title='title',
                time=datetime(2024, 7, 3, 16, 53),
                user_id='2348778469543521',
                server_id='897894654321546',
                is_private=False
            ),
            Remind(
                id='1234567890',
                title='title',
                time=datetime(2024, 8, 6, 0, 21),
                user_id='12348778469543521',
                server_id='1897894654321546',
                is_private=False
            )]
        
        self.server_id_to_channel_id = {
            '897894654321546': '123456789',
            '1897894654321546': '1234567890',
        }

        self.now = datetime(2024, 7, 3, 16, 52, 55)

    @patch('UseCases.Remind.NotifyRemind.RemindRepository')
    @patch('UseCases.Remind.NotifyRemind.datetime')
    def test_notify_remind_without_outputport(self, mock_remind_repository, mock_datetime):
            
            # Arrange
            mock_datetime.now.return_value = self.now
            repository = mock_remind_repository()
            mock_output_port = None
            notify_remind = NotifyRemind(repository, mock_output_port)
            notify_remind.close = False

            # Act
            async def run_test():
                await notify_remind.run()
                await notify_remind.stop()

            asyncio.run(run_test())

            # Assert
            self.assertEqual(notify_remind.close, True)

    @patch('UseCases.Remind.NotifyRemind.RemindRepository')
    @freeze_time('2024-08-07 16:52:57', tick=True)
    def test_notify_remind_with_outputport(self, mock_remind_repository):
            
            # Arrange
            repository = mock_remind_repository()
            mock_output_port_instance = AsyncMock(NotifyRemindOutputPort)
            notify_remind = NotifyRemind(repository, mock_output_port_instance)
            notify_remind.close = False
            repository.get_expired_reminds.return_value = self.reminds
            repository.get_channel_id_by_server_id.side_effect = lambda server_id: self.server_id_to_channel_id[server_id]  

            # Act
            async def run_test():
                async def stop():
                    await asyncio.sleep(3) # let the notify_remind run for 3 seconds
                    await notify_remind.stop()

                await asyncio.gather(stop(), notify_remind.run())

            asyncio.run(run_test())

            # Assert
            self.assertEqual(notify_remind.close, True)
            mock_output_port_instance.notify.assert_any_call(self.reminds[0], self.server_id_to_channel_id[self.reminds[0].server_id])
            mock_output_port_instance.notify.assert_any_call(self.reminds[1], self.server_id_to_channel_id[self.reminds[1].server_id])
            mock_output_port_instance.notify.assert_any_call(self.reminds[2], self.server_id_to_channel_id[self.reminds[2].server_id])



            
            


