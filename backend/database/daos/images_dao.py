from typing import List

from .base_dao import BaseDao
from core.dao_models.image import Image

TABLE = "images"
ID = "id"
PATH = "path"
COLUMNS = [ID, PATH]


class ImagesDao(BaseDao):
    def __init__(self):
        super().__init__(TABLE, COLUMNS)

    def get_images(self, ids: List[int] = None) -> List[Image]:
        if ids is not None:
            rows = self.get(clause="id in {}".format(self.list_to_in_param(ids)))
        else:
            rows = self.get()
        return [Image(**r) for r in rows]

    def insert_images(self, image_paths: List[str]) -> int:
        return self.insert([{PATH: i} for i in image_paths])


if __name__ == "__main__":
    id = ImagesDao()
    inserted = id.insert_images(["/test/path/1", "/test/path/2"])
    print(inserted)
    images = id.get_images()
    print(images)
