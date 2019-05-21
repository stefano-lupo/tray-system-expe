import random
import numpy as np
from typing import List, Tuple, Dict


from keras import layers, models, optimizers, applications
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.preprocessing.image import ImageDataGenerator

from .network import Network
from ..database.daos.ingredients_dao import IngredientsDao
from core.dao_models.ingredient import Ingredient

random.seed(0)



class IngredientDetector:
    def __init__(self):
        # TODO: This might end up moved into network
        self.ingredients: List[Ingredient] = IngredientsDao().get_ingredients()
        self.network = Network(num_classes=len(self.ingredients))

    def label(self, sub_image: np.ndarray) -> Ingredient:
        # TODO: Use NN here
        rand = random.random()
        if rand > 0.9:
            return random.choice(self.ingredients)

        return None
