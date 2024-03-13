import requests
import json

class GetBullShitAritcle:
    def __init__(self):
        self.api = 'https://api.howtobullshit.me/bullshit'

    def execute(self, topic, min_length):
        payload = {
            "Topic": topic,
            "MinLen": min_length
        }
        payload = json.dumps(payload)
        response = requests.post(
            url=self.api,
            data=payload,
            headers={
                "Content-Type": "application/json; charset=UTF-8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
            }
        )
        s = response.text
        s = s.replace('&nbsp;', '').replace('<br>', '')
        return s
