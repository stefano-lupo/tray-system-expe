import json
from typing import List, Dict
from datetime import datetime
from core.scan_request import ScanRequest

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Scan:

    def __init__(self,
                 menu_item_id: int,
                 image_id: int,
                 time: datetime = datetime.now(),
                 id: int = None,
                 user_id: int = None):
        self.id = id
        self.image_id = image_id
        self.menu_item_id = menu_item_id
        self.time = datetime.strptime(time, DATETIME_FORMAT) if isinstance(time, str) else time
        self.user_id = user_id

    @classmethod
    def from_scan_request(cls, scan_request: ScanRequest, image_id: int):
        return cls(scan_request.menu_item_id, image_id, user_id=scan_request.user_id)

    def get_as_dict(self):
        as_dict = dict(vars(self))
        as_dict['time'] = self.time.strftime(DATETIME_FORMAT)
        return as_dict

    def get_as_json(self):
        return json.dumps(self.get_as_dict())

    def get_for_insertion(self):
        as_dict = dict(vars(self))
        if self.user_id is None:
            as_dict.pop("user_id")

        return as_dict

