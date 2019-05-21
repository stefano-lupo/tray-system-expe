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
expected_shape = (1,32,32,3)

class IngredientDetector:
    def __init__(self):
        # TODO: This might end up moved into network
        self.ingredients: List[Ingredient] = IngredientsDao().get_ingredients()
        self.network = Network(num_classes=len(self.ingredients))

    def label(self, sub_image: np.ndarray) -> np.ndarray:
        expanded = np.expand_dims(sub_image, axis=0)
        shape = expanded.shape
        # if shape[0] is not 32 or shape[1] is not 32:
        #     print("Skipping")
        #     return None
        if shape != (1, 32, 32, 3):
            print("skipping")
            return None
        return self.network.predict(expanded)

