import cv2 as cv
import base64
import os
from uuid import uuid4

from backend.database.daos.detected_ingredients_dao import DetectedIngredientsDao
from backend.database.daos.images_dao import ImagesDao
from backend.database.daos.scans_dao import ScansDao
from backend.database.daos.master_dao import MasterDao
from backend.detection.detector import Detector
from core.dao_models.scan import Scan
from backend.database.daos.images_dao import ImagesDao
from core.scan_request import ScanRequest
from core.config import UPLOAD_DIR

def compute_file_name() -> str:
    # Comptue file name
    filename = base64.urlsafe_b64encode(uuid4().bytes)
    filename = filename.strip(b'=').decode('ascii')
    filename = str(filename) + ".jpg"
    full_path = os.path.join(UPLOAD_DIR, filename)
    return filename, full_path

class ScanHandler:

    def __init__(self):
        self.images_dao = ImagesDao()
        self.detected_ingredients_dao = DetectedIngredientsDao()
        self.scans_dao = ScansDao()
        self.detector = Detector()
    
    def hanlde_endpoint_scan(self, image, json) -> int:
        filename, full_path = compute_file_name()

        # Save the image using the flask file 
        image.save(full_path)

        scan_request = ScanRequest.from_request(json, filename)
        return self.handle_scan(scan_request, filename)

    def handle_local_scan(self, scan_request) -> int:
        filename, full_path = compute_file_name()
        cv.imwrite(full_path, scan_request.image)
        return self.handle_scan(scan_request, filename)

    def handle_scan(self, scan_request, image_path) -> int:
        image_id = self.images_dao.insert_images([image_path])

        # Upload scan to the db
        scan = Scan.from_scan_request(scan_request, image_id)
        scan.id = self.scans_dao.insert_scans([scan])

        detected_ingredients: List[DetectedIngredient] = self.detector.run_detection(scan_request, scan.id)
        self.detected_ingredients_dao.insert_detected_ingredients(detected_ingredients)

        return scan.id