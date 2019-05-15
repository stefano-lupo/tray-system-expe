from typing import List, Dict
from datetime import datetime

class Scan:

    def __init__(self,
                 id: int,
                 menu_item_id: int,
                 image_id: int,
                 time: datetime = datetime.now(),
                 user_id: int = None):
        self.id = id
        self.image_id = image_id
        self.menu_item_id = menu_item_id
        self.time = time
        self.user_id = user_id
        print("Scan constructor")

    def get_for_insertion(self):
        as_dict = vars(self)
        if self.user_id is None:
            as_dict.pop("user_id")

        return as_dict