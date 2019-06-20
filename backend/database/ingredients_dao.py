from typing import List

from .base_dao import BaseDao
from core.dao_models.ingredient import Ingredient

TABLE = "ingredients"
ID = "id"
NAME = "name"
COLUMNS = [ID, NAME]


class IngredientsDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)

    def get_ingredients(self) -> List[Ingredient]:
        rows = self.get()
        return [Ingredient(**r) for r in rows]

    def insert_ingredients(self, ingredients: List[Ingredient]) -> int:
        return self.insert([vars(i) for i in ingredients])
