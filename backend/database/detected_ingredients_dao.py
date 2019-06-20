from typing import List, Dict

from .base_dao import BaseDao
from core.dao_models.detection import Detection
from core.dao_models.detected_ingredient import DetectedIngredient
from core.dao_models.ingredient import INGREDIENT_ID_ALIAS, INGREDIENT_NAME_ALIAS
from core.dao_models.menu_item import MENU_ITEM_NAME_ALIAS
from core.dao_models.master_query_result import MasterQueryResult

TABLE = "detected_ingredients"
SCAN_ID = "scan_id"
INGREDIENT_ID = "ingredient_id"
DETECTIONS = "detections"
IMAGE_PATH = "image_path"
SQL_TIME_FORMAT = f = "%Y-%m-%d %H:%M:%S"
COLUMNS = [SCAN_ID, INGREDIENT_ID, DETECTIONS]


class DetectedIngredientsDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)

    def get_detected_ingredients(self, ids: List[int] = None) -> List[DetectedIngredient]:
        if ids is not None:
            rows = self.get(clause="scan_id in {}".format(self.list_to_in_param(ids)))
        else:
            rows = self.get()
        return [DetectedIngredient(**r) for r in rows]

    def insert_detected_ingredients(self, detected_ingredients: List[DetectedIngredient]) -> int:
        if len(detected_ingredients) == 0:
            print("No ingredients detected, skipping")
            return -1
        to_insert = []
        for d in detected_ingredients:
            json = d.get_as_json()
            to_insert.append(json)
        return self.insert(to_insert)


if __name__ == "__main__":
    did = DetectedIngredientsDao()
    d1 = Detection(0, 0, 100)
    d2 = Detection(40, 0, 50)
    detected_ingredient = DetectedIngredient(1, 1, [d1, d2])
    print(detected_ingredient.get_as_json())

    did.insert_detected_ingredients([detected_ingredient])
    did.insert_detected_ingredients([detected_ingredient])
    got = did.get_detected_ingredients()
    print(got)