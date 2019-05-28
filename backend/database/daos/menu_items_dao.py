from typing import Set
from collections import defaultdict

from .base_dao import BaseDao
from .ingredients_dao import IngredientsDao
from .menu_item_ingredient_dao import MenuItemIngredientDao
from core.dao_models.menu_item import *
from core.dao_models.ingredient import *

TABLE = "menu_items"
ID = "id"
NAME = "name"
COLUMNS = [ID, NAME]

MENU_ITEM_INGREDIENT_QUERY = \
    'select menu_items.id as {}, menu_items.name as {}, '.format(MENU_ITEM_ID_ALIAS, MENU_ITEM_NAME_ALIAS) + \
    'ingredients.id as {}, ingredients.name as {} '.format(INGREDIENT_ID_ALIAS, INGREDIENT_NAME_ALIAS) + \
    'from menu_item_ingredient ' \
    'inner join menu_items on menu_item_ingredient.menu_item_id = menu_items.id ' \
    'inner join ingredients on ingredients.id = menu_item_ingredient.ingredient_id '


class MenuItemsDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)
        self.ingredients_dao = IngredientsDao()
        self.menu_item_ingredient_dao = MenuItemIngredientDao()

    def get_menu_items(self, ids=None, names=None) -> List[MenuItem]:
        if ids is not None and names is not None:
            raise ValueError("IDs and names should not both be set")

        selector = None
        query_val = None
        if names is not None:
            selector = NAME
            query_val = self.comma_seperate(["'{}'".format(n) for n in names])
        elif ids is not None:
            selector = ID
            query_val = self.comma_seperate(ids)

        clause = "" if selector is None else 'where menu_items.{} in ({})'.format(selector, query_val)
        sql = MENU_ITEM_INGREDIENT_QUERY + clause
        rows = self.fetch_sql(sql)

        rows_by_menu_item = defaultdict(list)
        for row in rows:
            rows_by_menu_item[row[MENU_ITEM_ID_ALIAS]].append(row)

        return [MenuItem.from_db(r) for r in rows_by_menu_item.values()]

    def insert_menu_items(self, menu_items: List[MenuItem]):
        current_ingredients: Set[str] = set(tuple([i.name for i in self.ingredients_dao.get_ingredients()]))
        required_ingredients: Set[str] = set()
        for menu_item in menu_items:
            for ingredient in menu_item.ingredients:
                required_ingredients.add(ingredient.name)

        missing_ingredients = required_ingredients - current_ingredients

        if len(missing_ingredients) > 0:
            self.ingredients_dao.insert_ingredients([Ingredient(i) for i in missing_ingredients])

        ingredient_ids_by_name: Dict[str, int] = {i.name: i.id for i in self.ingredients_dao.get_ingredients()}

        for menu_item in menu_items:
            menu_item.id = self.insert([{NAME: menu_item.name}])
            ingredient_ids = [ingredient_ids_by_name[ingredient.name] for ingredient in menu_item.ingredients]
            self.menu_item_ingredient_dao.link_menu_item_to_ingredients(menu_item.id, ingredient_ids)
        return menu_items
