from Repository.Remind.RemindRepository import RemindRepository

class RemoveRemind:
    def __init__(self, repository: RemindRepository):
        self.repository = repository

    def execute(self, remind_id: str, server_id: str, user_id: str):
        reminds = self.repository.get_reminds_by_user_id(user_id)

        # Check
        # 1. does the remind_id exist
        # 2. does the remind_id belong to the user
        # 3. does the remind_id belong to the server

        remind = None
        for r in reminds:
            if r.id == remind_id:
                remind = r
                break

        if remind is None or remind.server_id != server_id or remind.user_id != user_id:
            raise ValueError('Remind not found')

        self.repository.remove(remind_id)