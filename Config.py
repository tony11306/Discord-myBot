from discord.activity import Game
from discord.enums import Status
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
COGS_FILE_PATH = os.getenv('COGS_FILE_PATH')
BOT_STATUS = Status.online
BOT_ACTIVITY = Game(name='會播音樂啦!')
JDOODLE_CLIENT_SECRET = os.getenv('JDOODLE_CLIENT_SECRET')
JDOODLE_CLIENT_CODE = os.getenv('JDOODLE_CLIENT_CODE')
YT_DLP_SERVER_URL = os.getenv('YT_DLP_SERVER_URL')