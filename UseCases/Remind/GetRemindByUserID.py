from typing import List

from Repository.Remind.RemindRepository import RemindRepository
from Model.Remind import Remind

class GetRemindByUserID:
    def __init__(self, repository: RemindRepository):
        self.repository = repository

    def execute(self, user_id: str) -> List[Remind]:
        return self.repository.get_reminds_by_user_id(user_id)