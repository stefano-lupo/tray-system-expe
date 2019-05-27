from typing import Dict
import jsonpickle as jp

from core.dao_models.scan import Scan
from core.dao_models.ingredient import Ingredient, INGREDIENT_ID_ALIAS, INGREDIENT_NAME_ALIAS
from core.dao_models.menu_item import MENU_ITEM_NAME_ALIAS, MENU_ITEM_ID_ALIAS
from core.dao_models.detection import Detection
from core.dao_models.detected_ingredient import DetectedIngredient


class MasterQueryResult:

    def __init__(self, row: Dict):
        self.ingredient = Ingredient(row[INGREDIENT_NAME_ALIAS], row[INGREDIENT_ID_ALIAS])
        self.menu_item_name = row[MENU_ITEM_NAME_ALIAS]
        self.scan = Scan(row[MENU_ITEM_ID_ALIAS], row["image_id"], row["time"], row["scan_id"], row["user_id"])
        detections = [Detection(**d) for d in jp.decode(row["detections"])]
        self.detected_ingredients = DetectedIngredient(self.scan.id, self.ingredient.id, detections)
