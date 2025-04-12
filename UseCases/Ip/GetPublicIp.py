from typing import Optional
from discord.ext import commands
import requests

class GetPublicIp:
    def __init__(self):
        pass

    def execute(self) -> Optional[str]:
        """Fetch and return the public IP address."""
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            return response.json().get("ip")
        except requests.RequestException as e:
            print(f"Error fetching public IP: {e}")
            return None