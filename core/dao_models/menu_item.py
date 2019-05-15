from typing import List, Dict

from dao_models.ingredient import *

MENU_ITEM_ID_ALIAS = "m_id"
MENU_ITEM_NAME_ALIAS = "m_name"

class MenuItem:

    def __init__(self, name: str, ingredients: List[Ingredient], id: int = None):
        self.name = name
        self.ingredients = ingredients
        self.id = id


    @classmethod
    def from_db(cls, db_rows: List[Dict]):
        if not db_rows:
            return None

        entry = db_rows[0]
        name: str = entry[MENU_ITEM_NAME_ALIAS]
        id: int = entry[MENU_ITEM_ID_ALIAS]
        ingredients = [Ingredient(row[INGREDIENT_NAME_ALIAS], row[INGREDIENT_ID_ALIAS]) for row in db_rows]
        return cls(name, ingredients, id)

    def __str__(self):
        return "{}".format(vars(self))
