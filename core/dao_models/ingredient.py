
INGREDIENT_ID_ALIAS = "ingredient_id"
INGREDIENT_NAME_ALIAS = "ingredient_name"

class Ingredient:

    def __init__(self, name: str, id: int = None):
        self.name = name
        self.id = id

    def __str__(self):
        return "{}".format(vars(self))
