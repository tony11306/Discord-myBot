from datetime import datetime

from Repository.Remind.RemindRepository import RemindRepository

class AddRemindArgs:
    def __init__(self, title: str, time: datetime, user_id: str, server_id: str, is_private: bool=False):
        self.title: str = title
        self.time: datetime = time
        self.user_id: str = user_id
        self.server_id: str = server_id
        self.is_private: bool = is_private

class AddRemind:
    def __init__(self, repository: RemindRepository):
        self.repository = repository

    def execute(self, args: AddRemindArgs) -> str:
        if self.repository.get_channel_id_by_server_id(args.server_id) is None:
            raise ValueError('Server is not set up for reminds')
        return self.repository.add(args.title, args.time, args.user_id, args.server_id, args.is_private)