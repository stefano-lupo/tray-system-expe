from enum import Enum

from core.config import API_PORT
BASE_URL = "http://localhost:{}".format(API_PORT)


class Endpoint(Enum):
    # Dont forget to add comma to end of this list
    SCAN = "/scan",
    WASTE_BY_MENU_ITEM = "/waste/menu_item",
    WASTE_BY_INGREDIENT = "/waste/ingredient",
    WASTE_PER_HOUR = "/waste/per_hour",
    WASTE_FOR_MENU_ITEM = "/waste/menu_item/<id>",

    RECENT_IMAGES = "/images/recent",
    IMAGE = "/image",

    DETECTIONS = "/detections",
    DETECTIONS_IMAGE = "/detections/image",

    def get(self) -> str:
        return BASE_URL + self.value[0]

    def get_without_prefix(self) -> str:
        without = self.value[0]
        print(without)
        return without

