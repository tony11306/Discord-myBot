from datetime import datetime

class Remind:
    def __init__(self, id: str, title: str, time: datetime, user_id: str, server_id: str, is_private: bool=False):
        self.id = id
        self.title = title
        self.time = time
        self.user_id = user_id
        self.server_id = server_id
        self.is_private = is_private

    def __eq__(self, other):
        if not isinstance(other, Remind):
            return False
        return self.id == other.id and self.title == other.title and self.time == other.time and self.user_id == other.user_id and self.server_id == other.server_id and self.is_private == other.is_private