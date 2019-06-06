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

    def transform_image_for_classification(image: np.ndarray):
        try:
            image = cv.cvtColor(copy, cv.COLOR_BGR2RGB)
        except:
            return None
        image = np.expand_dims(copy, axis=0)
        image = np.true_divide(copy, 255)

        if image.shape != EXPECTED_SHAPE:
            print("Skipping as shape was ")
            print(image.shape)
            return None
        
    def label(self, sub_image: np.ndarray) -> Ingredient:
        # copy = np.copy(sub_image)

        # if not len(copy):
        #     print("Skipping as copy was empty")
        #     return None

        
        predictions = self.network.predict(sub_image)
        index = np.argmax(predictions[0])
        return self.ingredients[index]

