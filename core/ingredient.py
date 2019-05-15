
INGREDIENT_ID_ALIAS = "i_id"
INGREDIENT_NAME_ALIAS = "i_name"

class Ingredient:

    def __init__(self, name: str, id: int = None):
        self.name = name
        self.id = id

    def __str__(self):
        return "{}".format(vars(self))
