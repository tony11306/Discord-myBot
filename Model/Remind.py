from datetime import datetime

class Remind:
    def __init__(self, id: str, title: str, time: datetime, user_id: str, server_id: str, is_private: bool=False):
        self.id = id
        self.title = title
        self.time = time
        self.user_id = user_id
        self.server_id = server_id
        self.is_private = is_private