from typing import List
import jsonpickle as jp

from dao_models.detection import Detection


class DetectedIngredient:
    def __init__(self, scan_id: int, ingredient_id: int, detections: List[Detection]):
        self.scan_id = scan_id
        self.ingredient_id = ingredient_id
        self.detections = detections

    def get_for_db(self):
        as_dict = vars(self)
        as_dict["detections"] = jp.encode(self.detections, unpicklable=False)
        return as_dict
