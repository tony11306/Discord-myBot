import unittest
from unittest.mock import patch

from UseCases.Google.GetNews import GetNews, GoogleNews

class TestGetNews(unittest.TestCase):
    
    @patch('requests.get')
    def test_get_news_default_count(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        with open('./tests/UseCases/Google/MockGetNewsData.html', 'r', encoding='utf-8') as f:
            mock_get.return_value.text = f.read()

        # Act
        get_news = GetNews()
        result = get_news.execute("elden ring")

        # Assert
        expected = [
            GoogleNews(title='George RR Martin 剛剛確認Elden Ring 改編正在製作中嗎？', link='https://news.google.com/articles/CBMicmh0dHBzOi8vd3d3LmdhbWVyZWFjdG9yLmNuL2RpZC1nZW9yZ2UtcnItbWFydGluLWp1c3QtY29uZmlybS10aGF0LWFuLWVsZGVuLXJpbmctYWRhcHRhdGlvbi1pcy1pbi10aGUtd29ya3MtODEwNjEzL9IBAA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='3 分鐘前', media='Gamereactor China'),
            GoogleNews(title='《艾爾登法環》釋出1.12.2 版規則更新調整「幽影樹庇佑」強化率上升曲線', link='https://news.google.com/articles/CBMiLWh0dHBzOi8vZ25uLmdhbWVyLmNvbS50dy9kZXRhaWwucGhwP3NuPTI2OTk0N9IBAA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='5 天前', media='巴哈姆特電玩資訊站'),
            GoogleNews(title='明日發售！《艾爾登法環Elden Ring》首部DLC「黃金樹幽影」發售宣傳片曝光', link='https://news.google.com/articles/CBMiWGh0dHBzOi8vaHlwZWJlYXN0LmNvbS9oay8yMDI0LzYvZWxkZW4tcmluZy1zaGFkb3ctb2YtdGhlLWVyZHRyZWUtb2ZmaWNpYWwtbGF1bmNoLXRyYWlsZXLSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='6月20日', media='HYPEBEAST'),
            GoogleNews(title='把大哥吹死，《黃金樹幽影》實況主用電子薩克斯風吹死DLC最終頭目', link='https://news.google.com/articles/CBMia2h0dHBzOi8vd3d3LjRnYW1lcnMuY29tLnR3L25ld3MvZGV0YWlsLzY1NjQxL3N0cmVhbWVyLXVzaW5nLWEtc2F4b3Bob25lLXRvLWRlZmVhdC1lbGRlbi1yaW5nLWRsYy1maW5hbC1ib3Nz0gEA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='3 小時前', media='4Gamers'),
            GoogleNews(title='超屈機指紋石盾流教學DLC變簡單模式輕鬆屈boss｜黃金樹幽影攻略', link='https://news.google.com/articles/CBMirAJodHRwczovL3d3dy5oazAxLmNvbS8lRTklODElOEElRTYlODglQjIlRTUlOEIlOTUlRTYlQkMlQUIvMTAzMjU3NS8lRTglQjYlODUlRTUlQjElODglRTYlQTklOUYlRTYlOEMlODclRTclQjQlOEIlRTclOUYlQjMlRTclOUIlQkUlRTYlQjUlODElRTYlOTUlOTklRTUlQUQlQjgtZGxjJUU4JUFFJThBJUU3JUIwJUExJUU1JTk2JUFFJUU2JUE4JUExJUU1JUJDJThGJUU4JUJDJTk1JUU5JUFDJTg2JUU1JUIxJTg4Ym9zcy0lRTklQkIlODMlRTklODclOTElRTYlQTglQjklRTUlQjklQkQlRTUlQkQlQjElRTYlOTQlQkIlRTclOTUlQTXSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='4 天前', media='香港01'),
            GoogleNews(title='《艾爾登法環》電影改編即將成真？喬治RR馬丁疑似在部落格暗示回應', link='https://news.google.com/articles/CBMiuQJodHRwczovL3R3Lm5ld3MueWFob28uY29tLyVFMyU4MCU4QSVFOCU4OSVCRSVFNyU4OCVCRSVFNyU5OSVCQiVFNiVCMyU5NSVFNyU5MiVCMCVFMyU4MCU4QiVFOSU5QiVCQiVFNSVCRCVCMSVFNiU5NCVCOSVFNyVCNyVBOCVFNSU4RCVCMyVFNSVCMCU4NyVFNiU4OCU5MCVFNyU5QyU5RiVFRiVCQyU5RiVFNSU5NiVBQyVFNiVCMiVCQnJyJUU5JUE2JUFDJUU0JUI4JTgxJUU3JTk2JTkxJUU0JUJDJUJDJUU1JTlDJUE4JUU5JTgzJUE4JUU4JTkwJUJEJUU2JUEwJUJDJUU2JTlBJTk3JUU3JUE0JUJBJUU1JTlCJTlFJUU2JTg3JTg5LTA0NDYzOTI5Ny5odG1s0gEA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='8 小時前', media='Yahoo奇摩新聞'),
            GoogleNews(title='《艾爾登法環》還真把大哥吹死了，實況主用電子薩克斯風全破DLC', link='https://news.google.com/articles/CBMiMWh0dHBzOi8vbmV3cy5nYW1lYmFzZS5jb20udHcvbmV3cy9kZXRhaWwvOTk0MjQ5MzDSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='6 小時前', media='遊戲基地'),
            GoogleNews(title='Elden Ring 艾爾登法環 DLC｜黃金樹幽影開啟路線、前置任務攻略', link='https://news.google.com/articles/CBMi5wFodHRwczovL2V6b25lLmhrL2FydGljbGUvMjAwMzYwMzYvRWxkZW4tUmluZy0lRTglODklQkUlRTclODglQkUlRTclOTklQkIlRTYlQjMlOTUlRTclOTIlQjAtRExDLSVFOSVCQiU4MyVFOSU4NyU5MSVFNiVBOCVCOSVFNSVCOSVCRCVFNSVCRCVCMSVFOSU5NiU4QiVFNSU5NSU5RiVFOCVCNyVBRiVFNyVCNyU5QS0lRTUlODklOEQlRTclQkQlQUUlRTQlQkIlQkIlRTUlOEIlOTklRTYlOTQlQkIlRTclOTUlQTXSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='5 天前', media='ezone.hk 即時科技生活新聞'),
            GoogleNews(title='「艾爾登法環黃金樹幽影」DLC來了！他喊「今天免請假40小時破關」 過來人打臉曝殘酷事實', link='https://news.google.com/articles/CBMiLmh0dHBzOi8vdGVjaC51ZG4uY29tL3RlY2gvc3RvcnkvMTIzMTU0LzgwNDM4NzHSATJodHRwczovL3RlY2gudWRuLmNvbS90ZWNoL2FtcC9zdG9yeS8xMjMxNTQvODA0Mzg3MQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='6月20日', media='科技玩家'),
            GoogleNews(title='《艾爾登法環》《機戰傭兵VI：境界天火》加入萬代南夢宮娛樂Steam 夏季特賣陣容', link='https://news.google.com/articles/CBMiLWh0dHBzOi8vZ25uLmdhbWVyLmNvbS50dy9kZXRhaWwucGhwP3NuPTI3MDA4NdIBAA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='3 天前', media='巴哈姆特電玩資訊站'),
        ]

        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_get_news_custom_count(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        with open('./tests/UseCases/Google/MockGetNewsData.html', 'r', encoding='utf-8') as f:
            mock_get.return_value.text = f.read()

        # Act
        get_news = GetNews()
        results = []
        for i in range(1, 11):
            results.append(get_news.execute("elden ring", i))

        # Assert
        expected_10 = [
            GoogleNews(title='George RR Martin 剛剛確認Elden Ring 改編正在製作中嗎？', link='https://news.google.com/articles/CBMicmh0dHBzOi8vd3d3LmdhbWVyZWFjdG9yLmNuL2RpZC1nZW9yZ2UtcnItbWFydGluLWp1c3QtY29uZmlybS10aGF0LWFuLWVsZGVuLXJpbmctYWRhcHRhdGlvbi1pcy1pbi10aGUtd29ya3MtODEwNjEzL9IBAA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='3 分鐘前', media='Gamereactor China'),
            GoogleNews(title='《艾爾登法環》釋出1.12.2 版規則更新調整「幽影樹庇佑」強化率上升曲線', link='https://news.google.com/articles/CBMiLWh0dHBzOi8vZ25uLmdhbWVyLmNvbS50dy9kZXRhaWwucGhwP3NuPTI2OTk0N9IBAA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='5 天前', media='巴哈姆特電玩資訊站'),
            GoogleNews(title='明日發售！《艾爾登法環Elden Ring》首部DLC「黃金樹幽影」發售宣傳片曝光', link='https://news.google.com/articles/CBMiWGh0dHBzOi8vaHlwZWJlYXN0LmNvbS9oay8yMDI0LzYvZWxkZW4tcmluZy1zaGFkb3ctb2YtdGhlLWVyZHRyZWUtb2ZmaWNpYWwtbGF1bmNoLXRyYWlsZXLSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='6月20日', media='HYPEBEAST'),
            GoogleNews(title='把大哥吹死，《黃金樹幽影》實況主用電子薩克斯風吹死DLC最終頭目', link='https://news.google.com/articles/CBMia2h0dHBzOi8vd3d3LjRnYW1lcnMuY29tLnR3L25ld3MvZGV0YWlsLzY1NjQxL3N0cmVhbWVyLXVzaW5nLWEtc2F4b3Bob25lLXRvLWRlZmVhdC1lbGRlbi1yaW5nLWRsYy1maW5hbC1ib3Nz0gEA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='3 小時前', media='4Gamers'),
            GoogleNews(title='超屈機指紋石盾流教學DLC變簡單模式輕鬆屈boss｜黃金樹幽影攻略', link='https://news.google.com/articles/CBMirAJodHRwczovL3d3dy5oazAxLmNvbS8lRTklODElOEElRTYlODglQjIlRTUlOEIlOTUlRTYlQkMlQUIvMTAzMjU3NS8lRTglQjYlODUlRTUlQjElODglRTYlQTklOUYlRTYlOEMlODclRTclQjQlOEIlRTclOUYlQjMlRTclOUIlQkUlRTYlQjUlODElRTYlOTUlOTklRTUlQUQlQjgtZGxjJUU4JUFFJThBJUU3JUIwJUExJUU1JTk2JUFFJUU2JUE4JUExJUU1JUJDJThGJUU4JUJDJTk1JUU5JUFDJTg2JUU1JUIxJTg4Ym9zcy0lRTklQkIlODMlRTklODclOTElRTYlQTglQjklRTUlQjklQkQlRTUlQkQlQjElRTYlOTQlQkIlRTclOTUlQTXSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='4 天前', media='香港01'),
            GoogleNews(title='《艾爾登法環》電影改編即將成真？喬治RR馬丁疑似在部落格暗示回應', link='https://news.google.com/articles/CBMiuQJodHRwczovL3R3Lm5ld3MueWFob28uY29tLyVFMyU4MCU4QSVFOCU4OSVCRSVFNyU4OCVCRSVFNyU5OSVCQiVFNiVCMyU5NSVFNyU5MiVCMCVFMyU4MCU4QiVFOSU5QiVCQiVFNSVCRCVCMSVFNiU5NCVCOSVFNyVCNyVBOCVFNSU4RCVCMyVFNSVCMCU4NyVFNiU4OCU5MCVFNyU5QyU5RiVFRiVCQyU5RiVFNSU5NiVBQyVFNiVCMiVCQnJyJUU5JUE2JUFDJUU0JUI4JTgxJUU3JTk2JTkxJUU0JUJDJUJDJUU1JTlDJUE4JUU5JTgzJUE4JUU4JTkwJUJEJUU2JUEwJUJDJUU2JTlBJTk3JUU3JUE0JUJBJUU1JTlCJTlFJUU2JTg3JTg5LTA0NDYzOTI5Ny5odG1s0gEA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='8 小時前', media='Yahoo奇摩新聞'),
            GoogleNews(title='《艾爾登法環》還真把大哥吹死了，實況主用電子薩克斯風全破DLC', link='https://news.google.com/articles/CBMiMWh0dHBzOi8vbmV3cy5nYW1lYmFzZS5jb20udHcvbmV3cy9kZXRhaWwvOTk0MjQ5MzDSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='6 小時前', media='遊戲基地'),
            GoogleNews(title='Elden Ring 艾爾登法環 DLC｜黃金樹幽影開啟路線、前置任務攻略', link='https://news.google.com/articles/CBMi5wFodHRwczovL2V6b25lLmhrL2FydGljbGUvMjAwMzYwMzYvRWxkZW4tUmluZy0lRTglODklQkUlRTclODglQkUlRTclOTklQkIlRTYlQjMlOTUlRTclOTIlQjAtRExDLSVFOSVCQiU4MyVFOSU4NyU5MSVFNiVBOCVCOSVFNSVCOSVCRCVFNSVCRCVCMSVFOSU5NiU4QiVFNSU5NSU5RiVFOCVCNyVBRiVFNyVCNyU5QS0lRTUlODklOEQlRTclQkQlQUUlRTQlQkIlQkIlRTUlOEIlOTklRTYlOTQlQkIlRTclOTUlQTXSAQA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='5 天前', media='ezone.hk 即時科技生活新聞'),
            GoogleNews(title='「艾爾登法環黃金樹幽影」DLC來了！他喊「今天免請假40小時破關」 過來人打臉曝殘酷事實', link='https://news.google.com/articles/CBMiLmh0dHBzOi8vdGVjaC51ZG4uY29tL3RlY2gvc3RvcnkvMTIzMTU0LzgwNDM4NzHSATJodHRwczovL3RlY2gudWRuLmNvbS90ZWNoL2FtcC9zdG9yeS8xMjMxNTQvODA0Mzg3MQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='6月20日', media='科技玩家'),
            GoogleNews(title='《艾爾登法環》《機戰傭兵VI：境界天火》加入萬代南夢宮娛樂Steam 夏季特賣陣容', link='https://news.google.com/articles/CBMiLWh0dHBzOi8vZ25uLmdhbWVyLmNvbS50dy9kZXRhaWwucGhwP3NuPTI3MDA4NdIBAA?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant', time='3 天前', media='巴哈姆特電玩資訊站'),
        ]
        expecteds = [expected_10[:i] for i in range(1, 11)]

        self.assertEqual(results, expecteds)

    @patch('requests.get')
    def test_get_news_negative_count(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = 200
        with open('./tests/UseCases/Google/MockGetNewsData.html', 'r', encoding='utf-8') as f:
            mock_get.return_value.text = f.read()

        # Act
        get_news = GetNews()
        result = get_news.execute("elden ring", -5)

        # Assert
        expected = []

        self.assertEqual(result, expected)
