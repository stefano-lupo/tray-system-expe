from typing import List, Dict

from .base_dao import BaseDao

TABLE = "menu_item_ingredient"
MENU_ITEM_ID = "menu_item_id"
INGREDIENT_ID = "ingredient_id"
COLUMNS = [MENU_ITEM_ID, INGREDIENT_ID]


class MenuItemIngredientDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)

    def link_menu_item_to_ingredients(self, menu_item_id: int, ingredient_ids: List[int]) -> int:
        links: List[Dict[str, int]] = [{MENU_ITEM_ID: menu_item_id, INGREDIENT_ID: iid} for iid in ingredient_ids]
        return self.insert(links)
