from typing import List

from .base_dao import BaseDao
from core.dao_models.scan import Scan

TABLE = "scans"
ID = "id"
MENU_ITEM_ID = "menu_item_id"
IMAGE_ID = "image_id"
TIME = "time"
USER_ID = "user_id"
COLUMNS = [ID, MENU_ITEM_ID, IMAGE_ID, TIME, USER_ID]


class ScansDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)

    def get_scans(self, ids: List[int] = None) -> List[Scan]:
        if ids is not None:
            rows = self.get(clause="ids in {}".format(self.list_to_in_param(ids)))
        else:
            rows = self.get()
        return [Scan(**r) for r in rows]

    def insert_scans(self, scans: List[Scan]) -> int:
        return self.insert([s.get_for_insertion() for s in scans])


if __name__ == "__main__":
    sd = ScansDao()
    # scan = Scan(1, 1, 1)
    # sd.insert_scans([scan])
    # sd.get_scans()
