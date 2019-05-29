from typing import List, Dict
from collections import defaultdict
import json
# import jsonpickle as jp

from .detection import Detection


class DetectedIngredient:
    def __init__(self, scan_id: int, ingredient_id: int, detections: List[Detection]):
        self.scan_id = scan_id
        self.ingredient_id = ingredient_id
        self.detections = detections

    def get_total_waste(self) -> int:
        return sum([d.mass for d in self.detections])

    def get_as_dict(self):
        as_dict = dict(vars(self))
        as_dict["detections"] = [d.get_as_dict() for d in self.detections]
        return as_dict

    def get_as_json(self):
        as_dict = dict(vars(self))
        as_dict["detections"] = json.dumps([d.get_as_dict() for d in self.detections])
        return as_dict
