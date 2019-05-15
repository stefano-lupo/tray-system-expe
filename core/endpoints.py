from enum import Enum
from typing import Dict

from core.config import API_PORT
BASE_URL = "http://localhost:{}".format(API_PORT)


class Endpoint(Enum):
    SCAN = "/scan",
    SOMETHING_ELSE = "/else"

    def get(self) -> str:
        return BASE_URL + self.value[0]

    def get_without_prefix(self) -> str:
        return self.value[0]

