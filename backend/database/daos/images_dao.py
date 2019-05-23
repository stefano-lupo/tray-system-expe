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

    def get_ingredients_in_image(self, image_id):
        sql = 'select detected_ingredients.ingredient_id, detected_ingredients.detections, images.id f' \
              'rom detected_ingredients ' \
              'inner join scans on detected_ingredients.scan_id = scans.id ' \
              'inner join images on scans.image_id = images.id where images.id = {}'.format(image_id)
        return self.fetch_sql(sql)


if __name__ == "__main__":
    id = ImagesDao()
    inserted = id.insert_images(["/test/path/1", "/test/path/2"])
    print(inserted)
    images = id.get_images()
    print(images)
