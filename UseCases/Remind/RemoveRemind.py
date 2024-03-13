from Repository.Remind.RemindRepository import RemindRepository

class RemoveRemind:
    def __init__(self, repository: RemindRepository):
        self.repository = repository

    def execute(self, id: str):
        self.repository.remove(id)