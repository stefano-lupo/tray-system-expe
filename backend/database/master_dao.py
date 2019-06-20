from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta

from backend.database.daos.base_dao import BaseDao
from core.dao_models.master_query_result import MasterQueryResult
from core.dao_models.scan_with_data import ScanWithData
from core.dao_models.menu_item import MENU_ITEM_NAME_ALIAS, MENU_ITEM_ID_ALIAS
from core.dao_models.ingredient import INGREDIENT_NAME_ALIAS, INGREDIENT_ID_ALIAS

TABLE = "master"
COLUMNS = ["scan_id", "detections",
           "menu_item_id", "menu_item_name",
           "ingredient_id", "ingredient_name",
           "image_id", "user_id", "time"]


class MasterDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)

    def get_rows(self, ids: List[int] = None) -> List[MasterQueryResult]:
        if ids is not None:
            rows = self.get(clause="scan_id in {}".format(self.list_to_in_param(ids)))
        else:
            rows = self.get()

        return [MasterQueryResult(row) for row in rows]

    def get_by_ids(self, ids: List[int] = None) -> Dict[id, List[MasterQueryResult]]:
       rows: List[MasterQueryResult] = self.get_rows(ids)
       by_scan_id: Dict = defaultdict(list)
       for row in rows:
           by_scan_id[row.scan.id].append(row)
       return by_scan_id

    def get_recent(self, time_delta_hours=24):
        # TODO:24
        return {k: ScanWithData(v) for (k, v) in self.get_by_ids().items()}

    def get_waste_by_menu_item(self):
        rows: List[MasterQueryResult] = self.get_rows()
        food_waste_by_menu_item: Dict[str, int] = defaultdict(int)
        for row in rows:
            food_waste_by_menu_item[row.menu_item_name] = \
                food_waste_by_menu_item[row.menu_item_name] + row.detected_ingredients.get_total_waste()
        return food_waste_by_menu_item

    def get_waste_by_ingredient(self):
        rows: List[MasterQueryResult] = self.get_rows()
        food_waste_by_ingredient: Dict[str, int] = defaultdict(int)
        for row in rows:
            food_waste_by_ingredient[row.ingredient.name] = \
                food_waste_by_ingredient[row.ingredient.name] + row.detected_ingredients.get_total_waste()
        return food_waste_by_ingredient

    def get_waste_per_hour(self) -> Dict:
        rows: List[MasterQueryResult] = self.get_rows()
        mass_by_timestamp = {row.scan.time: row.detected_ingredients.get_total_waste() for row in rows}
        last_twelve_hours = datetime.now() - timedelta(hours=12)
        mass_by_timestamp = {int(k.timestamp()): v for (k, v) in mass_by_timestamp.items() if k >= last_twelve_hours}

        return mass_by_timestamp

    def get_detections_by_scan_id(self, scan_ids: List[int] = None) -> Dict:
        by_scan_id: Dict[int, List[MasterQueryResult]] = self.get_by_ids(scan_ids)
        detections_by_scan_id = defaultdict(dict)
        for scan_id, mqrs in by_scan_id.items():
            for mqr in mqrs:
                detections_by_scan_id[mqr.ingredient.id] = mqr.detected_ingredients
        return detections_by_scan_id


if __name__ == "__main__":
    md = MasterDao()
    d = md.get_detections_by_scan_id()
    print(d)
