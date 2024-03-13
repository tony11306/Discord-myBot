from Repository.Remind.RemindRepository import RemindRepository

class UnbindRemindChannel:
    def __init__(self, repository: RemindRepository):
        self.repository = repository

    def execute(self, server_id: str):
        if self.repository.get_channel_id_by_server_id(server_id) is None:
            raise ValueError('Server is not set up for reminds')
        self.repository.remove_remind_channel(server_id)