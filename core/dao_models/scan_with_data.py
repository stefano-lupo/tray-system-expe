from typing import List
from .detected_ingredient import DetectedIngredient
from .master_query_result import MasterQueryResult
from .scan import Scan

import json


class ScanWithData:

    def __init__(self, mqrs: List[MasterQueryResult]):
        self.scan: Scan = mqrs[0].scan
        self.menu_item_name: str = mqrs[0].menu_item_name
        self.detected_ingredients: List[DetectedIngredient] = [mqr.detected_ingredients for mqr in mqrs]
        self.waste_by_ingredient = {}
        for di in self.detected_ingredients:
            self.waste_by_ingredient[di.ingredient_id] = sum([d.mass for d in di.detections])

    def get_as_dict(self):
        as_dict = dict(vars(self))
        as_dict['detected_ingredients'] = [di.get_as_dict() for di in self.detected_ingredients]
        # as_dict['ingredient'] = self.ingredient.get_as_dict()
        as_dict['scan'] = self.scan.get_as_dict()
        return as_dict

    def get_as_json(self):
        return json.dumps(self.get_as_dict())