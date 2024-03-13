import sqlite3
from datetime import datetime
from typing import List

class VoiceTextChannelRepository:
    def __init__(self):
        pass

    def add_relation(self, text_channel_id: str, voice_channel_id: str):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO VoiceTextChannel (text_channel_id, voice_channel_id) VALUES (?, ?)', (text_channel_id, voice_channel_id))
        conn.commit()
        conn.close()
    
    def remove_relation(self, text_channel_id: str, voice_channel_id: str):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM VoiceTextChannel WHERE text_channel_id = ? AND voice_channel_id = ?', (text_channel_id, voice_channel_id))
        conn.commit()
        conn.close()

    def get_text_channel_ids_by_voice_channel_id(self, voice_channel_id: str) -> List[str]:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT text_channel_id FROM VoiceTextChannel WHERE voice_channel_id = ?', (voice_channel_id,))
        text_channel_ids = cursor.fetchall()
        conn.close()
        return [text_channel_id[0] for text_channel_id in text_channel_ids]
