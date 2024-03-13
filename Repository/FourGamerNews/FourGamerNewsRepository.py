import sqlite3
from typing import List

class FourGamerNewsRepository:
    def __init__(self):
        pass

    def add_text_channel(self, text_channel_id: str):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO FourGamerNewsBroadcastChannel (channel_id) VALUES (?)', (text_channel_id,))
        conn.commit()
        conn.close()

    def remove_text_channel(self, text_channel_id: str):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM FourGamerNewsBroadcastChannel WHERE channel_id = ?', (text_channel_id,))
        conn.commit()
        conn.close()

    def get_text_channels(self) -> List[str]:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT channel_id FROM FourGamerNewsBroadcastChannel')
        text_channels = cursor.fetchall()
        conn.close()
        return [text_channel[0] for text_channel in text_channels]