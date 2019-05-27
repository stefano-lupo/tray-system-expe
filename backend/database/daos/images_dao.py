from typing import List

from backend.database.daos.base_dao import BaseDao
from backend.database.daos.scans_dao import ScansDao
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
            clause = "id in {}".format(self.list_to_in_param(ids))
            rows = self.get(clause=clause)
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


    def get_path(self, image_id, scan_id):
        if image_id is not None:
            return self.get_images([image_id])[0].path
        else:
            sql = 'select images.path from images ' \
                'inner join scans on scans.image_id = images.id ' \
                'where scans.id = {}'.format(scan_id)
            return self.fetch_sql(sql)[0]['path']

if __name__ == "__main__":
    id = ImagesDao()
    path = id.get_path(1, None)
    print(path)
    # inserted = id.insert_images(["/test/path/1", "/test/path/2"])
    # print(inserted)
    # images = id.get_images()
    # print(images)
