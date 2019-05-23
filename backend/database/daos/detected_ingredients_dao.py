from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta

import jsonpickle as jp
import numpy as np

from .base_dao import BaseDao
from core.dao_models.detection import Detection
from core.dao_models.detected_ingredient import DetectedIngredient
from core.dao_models.scan import Scan
from core.dao_models.ingredient import Ingredient, INGREDIENT_ID_ALIAS, INGREDIENT_NAME_ALIAS
from core.dao_models.menu_item import MenuItem, MENU_ITEM_NAME_ALIAS, MENU_ITEM_ID_ALIAS

TABLE = "detected_ingredients"
SCAN_ID = "scan_id"
INGREDIENT_ID = "ingredient_id"
DETECTIONS = "detections"
IMAGE_PATH = "image_path"
SQL_TIME_FORMAT = f = "%Y-%m-%d %H:%M:%S"
COLUMNS = [SCAN_ID, INGREDIENT_ID, DETECTIONS]


class MasterQueryResult:

    def __init__(self, row: Dict):
        self.ingredient = Ingredient(row[INGREDIENT_NAME_ALIAS], row[INGREDIENT_ID_ALIAS])
        self.menu_item_name = row[MENU_ITEM_NAME_ALIAS]
        self.scan = Scan(row[MENU_ITEM_ID_ALIAS], row["image_id"], row["time"], row["id"], row["user_id"])
        detections = [Detection(**d) for d in jp.decode(row["detections"])]
        self.detected_ingredients = DetectedIngredient(self.scan.id, self.ingredient.id, detections)


class DetectedIngredientsDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)

    def get_detected_ingredients(self, ids: List[int] = None) -> List[DetectedIngredient]:
        if ids is not None:
            rows = self.get(clause="id in {}".format(self.list_to_in_param(ids)))
        else:
            rows = self.get()
        return [DetectedIngredient(**r) for r in rows]

    def get_waste_by_menu_item(self):
        rows: List[MasterQueryResult] = self.master_query()
        food_waste_by_menu_item: Dict[str, int] = defaultdict(int)
        for row in rows:
            food_waste_by_menu_item[row.menu_item_name] =  \
                food_waste_by_menu_item[row.menu_item_name] + row.detected_ingredients.get_total_waste()
        return food_waste_by_menu_item

    def get_waste_by_ingredient(self):
        rows: List[MasterQueryResult] = self.master_query()
        food_waste_by_ingredient: Dict[str, int] = defaultdict(int)
        for row in rows:
            food_waste_by_ingredient[row.ingredient.name] =  \
                food_waste_by_ingredient[row.ingredient.name] + row.detected_ingredients.get_total_waste()
        return food_waste_by_ingredient

    def get_waste_per_hour(self) -> Dict:
        rows: List[MasterQueryResult] = self.master_query()
        mass_by_timestamp = {row.scan.time: row.detected_ingredients.get_total_waste() for row in rows}
        last_twelve_hours = datetime.now() - timedelta(hours=12)
        mass_by_timestamp = {int(k.timestamp()): v for (k, v) in mass_by_timestamp.items() if k >= last_twelve_hours}

        return mass_by_timestamp

    def insert_detected_ingredients(self, detected_ingredients: List[DetectedIngredient]) -> int:
        if len(detected_ingredients) == 0:
            print("No ingredients detected, skipping")
            return
        return self.insert([d.get_for_db() for d in detected_ingredients])

    def master_query(self) -> List[MasterQueryResult]:
        sql = 'select ' \
              'detected_ingredients.detections,' \
              'scans.*, ' \
              'ingredients.name as {}, ingredients.id as {},'.format(INGREDIENT_NAME_ALIAS, INGREDIENT_ID_ALIAS) + \
              'menu_items.name as {} '.format(MENU_ITEM_NAME_ALIAS) + \
              'from detected_ingredients ' \
              'inner join ingredients on ingredients.id = detected_ingredients.ingredient_id ' \
              'inner join scans on scans.id = detected_ingredients.scan_id ' \
              'inner join menu_items on menu_items.id = scans.menu_item_id '
        print(sql)

        return [MasterQueryResult(row) for row in self.fetch_sql(sql)]


if __name__ == "__main__":
    did = DetectedIngredientsDao()
    d1 = Detection(0, 0, 100)
    d2 = Detection(40, 0, 50)
    detected_ingredient = DetectedIngredient(1, 1, [d1, d2])
    print(detected_ingredient.get_for_db())

    did.insert_detected_ingredients([detected_ingredient])
    did.insert_detected_ingredients([detected_ingredient])
    got = did.get_detected_ingredients()
    print(got)