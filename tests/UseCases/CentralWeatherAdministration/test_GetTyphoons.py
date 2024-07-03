import unittest
from unittest.mock import patch

from UseCases.CentralWeatherAdministration.GetTyphoons import GetTyphoons, Typhoon

class TestGetTyphoons(unittest.TestCase):

    @patch('selenium.webdriver.Chrome')
    def test_get_typhoons_no_typhoon(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        with open('./tests/UseCases/CentralWeatherAdministration/MockGetTyphoonsData1.html', 'r', encoding='utf-8') as f:
            mock_get.return_value.page_source = f.read()

        # Act
        get_typhoons = GetTyphoons()
        result = get_typhoons.execute()

        # Assert
        expected = []
        self.assertEqual(result, expected)