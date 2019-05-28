import random
import numpy as np
import cv2 as cv
from typing import List

from backend.detection.network import Network
from ..database.daos.ingredients_dao import IngredientsDao
from core.dao_models.ingredient import Ingredient
from core.config import IMAGE_SEGMENT_SIZE_PX

random.seed(0)
EXPECTED_SHAPE = (1, IMAGE_SEGMENT_SIZE_PX, IMAGE_SEGMENT_SIZE_PX, 3)


class IngredientDetector:
    def __init__(self):
        self.ingredients: List[Ingredient] = IngredientsDao().get_ingredients()
        self.network = Network()

    def label(self, sub_image: np.ndarray) -> Ingredient:
        copy = np.copy(sub_image)

        if not len(copy):
            print("Skipping as copy was empty")
            return None

        try:
            copy = cv.cvtColor(copy, cv.COLOR_BGR2RGB)
        except:
            return None
        copy = np.expand_dims(copy, axis=0)
        copy = np.true_divide(copy, 255)

        if copy.shape != EXPECTED_SHAPE:
            print("Skipping as shape was ")
            print(copy.shape)
            return None
        predictions = self.network.predict(copy)
        index = np.argmax(predictions[0])
        return self.ingredients[index]

