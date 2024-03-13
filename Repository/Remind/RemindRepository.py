import sqlite3
from datetime import datetime
from typing import List

from Model.Remind import Remind

class RemindRepository:
    '''
    I do not handle timezone issues here, since it's quite small personal used bot.
    '''
    def __init__(self):
        pass
    
    def add(self, title: str, time: datetime, user_id: str, server_id: str, is_private: bool) -> str:
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute('INSERT INTO Remind (title, time, user_id, server_id, is_private) VALUES (?, ?, ?, ?, ?)', (title, time, user_id, server_id, is_private))
        conn.commit()
        conn.close()
        return str(c.lastrowid)
    
    def remove(self, id: str):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute('DELETE FROM Remind WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def get_reminds_by_user_id(self, user_id: str) -> List[Remind]:
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Remind WHERE user_id = ?', (user_id,))
        reminds = c.fetchall()
        conn.close()
        return [Remind(remind[0], remind[2], remind[1], remind[4], remind[5], remind[3]) for remind in reminds]
    
    def get_expired_reminds(self) -> List[Remind]:
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Remind WHERE time <= ?', (datetime.now(),))
        reminds = c.fetchall()
        conn.close()
        return [Remind(remind[0], remind[2], remind[1], remind[4], remind[5], remind[3]) for remind in reminds]
    
    def get_channel_id_by_server_id(self, server_id: str) -> str:
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute('SELECT channel_id FROM ServerRemindChat WHERE server_id = ?', (server_id,))
        channel_id = c.fetchone()
        conn.close()
        return channel_id[0] if channel_id else None
    
    def add_remind_channel(self, server_id: str, channel_id: str):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute('INSERT INTO ServerRemindChat (server_id, channel_id) VALUES (?, ?)', (server_id, channel_id))
        conn.commit()
        conn.close()

    def remove_remind_channel(self, server_id: str):
        conn = sqlite3.connect('db.db')
        c = conn.cursor()
        c.execute('DELETE FROM ServerRemindChat WHERE server_id = ?', (server_id,))
        conn.commit()
        conn.close()