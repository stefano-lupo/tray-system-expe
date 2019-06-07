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

    def transform_image_for_classification(self, image: np.ndarray):
        copy = np.copy(image)
        try:
            copy = cv.cvtColor(copy, cv.COLOR_BGR2RGB)
        except:
            print("Couldnt convert colour")
            return None

        # image = np.expand_dims(image, axis=0)
        copy = np.true_divide(copy, 255)

        # if image.shape != EXPECTED_SHAPE:
        #     print("Skipping as shape was ")
        #     print(image.shape)
        #     return None
        return copy

    def predict(self, sub_image):
        sub_image = np.expand_dims(sub_image, axis=0)
        if sub_image.shape != EXPECTED_SHAPE:
            print("Skipping as shape was ")
            print(sub_image.shape)
            return None

        return self.network.predict(sub_image)


    def label(self, sub_image: np.ndarray) -> Ingredient:
        # copy = np.copy(sub_image)

        # if not len(copy):
        #     print("Skipping as copy was empty")
        #     return None

        predictions = self.predict(sub_image)
        # print(predictions)
        if predictions is None:
            return None
        index = np.argmax(predictions[0])
        return self.ingredients[index]

