from typing import List, Dict

import jsonpickle as jp
import numpy as np
import cv2 as cv


class ScanRequest:

    def __init__(self,
                 image: np.ndarray,
                 depth_map: np.ndarray,
                 menu_item_id: int,
                 user_id: int = None):
        self.image = image
        self.depth_map = depth_map
        self.menu_item_id = menu_item_id
        self.user_id = user_id

    @classmethod
    def from_request(cls, json: str, image_path: str):
        as_dict = jp.decode(json)
        as_dict["image"] = cv.imread(image_path)
        return cls(**as_dict)

    def get_files(self):
        return {
            "image": self.image,
        }

    def remove_matrices(self) -> Dict:
        as_dict = dict(vars(self))
        as_dict.pop("image")
        as_dict["depth_map"] = self.depth_map.tolist()

        return as_dict

    def get_json(self) -> str:
        return jp.encode(self.remove_matrices(), unpicklable=False)


    def get_for_insertion(self):
        return self.remove_matrices()
