from typing import List

class ScanRequest:

    def __init__(self,
                 image,
                 depth_map: List[List[int]],
                 menu_item_id: int,
                 user_id: int = None):
        self.image = image
        self.depth_map = depth_map
        self.menu_item_id = menu_item_id
        self.user_id = user_id
