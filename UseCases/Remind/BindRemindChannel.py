from Repository.Remind.RemindRepository import RemindRepository

class BindRemindChannel:
    def __init__(self, repository: RemindRepository):
        self.repository = repository

    def execute(self, server_id: str, channel_id: str):
        if self.repository.get_channel_id_by_server_id(server_id) is not None:
            raise ValueError('Server is already set up for reminds')
        self.repository.add_remind_channel(server_id, channel_id)