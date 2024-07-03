import unittest
from unittest.mock import patch

from UseCases.CentralWeatherAdministration.GetRecentQuakes import GetRecentQuakes, Quake

class TestGetRecentQuakes(unittest.TestCase):
    @patch('requests.get')
    def test_get_recent_quakes(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        with open('./tests/UseCases/CentralWeatherAdministration/MockGetRecentQuakesData.html', 'r', encoding='utf-8') as f:
            mock_get.return_value.text = f.read()

        # Act
        get_recent_quakes = GetRecentQuakes()
        result = get_recent_quakes.execute()

        # Assert
        expected = [
            Quake(location='位於花蓮縣近海', magnitude='3.6', level='3級', depth='8.8km', time='07/01 20:06NEW'),
            Quake(location='位於花蓮縣近海', magnitude='3.4', level='3級', depth='9.7km', time='07/01 13:00NEW'),
            Quake(location='位於臺灣東部海域', magnitude='3.7', level='2級', depth='28.9km', time='07/01 05:09'),
            Quake(location='位於花蓮縣秀林鄉', magnitude='3.8', level='2級', depth='32.4km', time='07/01 00:45'),
            Quake(location='位於臺灣東部海域', magnitude='3.8', level='2級', depth='9.7km', time='06/30 14:52'),
        ]

        self.assertEqual(result, expected)


        


