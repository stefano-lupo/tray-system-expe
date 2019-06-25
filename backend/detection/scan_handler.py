import cv2 as cv
import base64
import os
import timeit
from uuid import uuid4
from typing import List
import requests

from backend.database.detected_ingredients_dao import DetectedIngredientsDao
from backend.database.images_dao import ImagesDao
from backend.database.scans_dao import ScansDao
from backend.database.master_dao import MasterDao
from backend.detection.detector import Detector
from core.dao_models.scan import Scan
from core.dao_models.detected_ingredient import DetectedIngredient
from backend.database.images_dao import ImagesDao
from core.scan_request import ScanRequest
from core.config import UPLOAD_DIR, LORENZO_URL

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

        start = timeit.default_timer()
        cv.imwrite(full_path, scan_request.image)
        stop = timeit.default_timer()
        print("Took %s seconds to write image" % str(stop - start))
        return self.handle_scan(scan_request, filename)

    def handle_scan(self, scan_request, image_path) -> int:
        image_id = self.images_dao.insert_images([image_path])

        # Upload scan to the db
        scan = Scan.from_scan_request(scan_request, image_id)
        scan.id = self.scans_dao.insert_scans([scan])

        start = timeit.default_timer()
        detected_ingredients: List[DetectedIngredient] = self.detector.run_detection(scan_request, scan.id)
        stop = timeit.default_timer()
        print("Took %s to detect all ingredients" % (stop - start))
        
        self.detected_ingredients_dao.insert_detected_ingredients(detected_ingredients)
        score = sum([di.get_total_waste() for di in detected_ingredients])
        print("Had food waste score {}", score)
        r = requests.post(LORENZO_URL + "/" + str(scan.id), data={'score': score})
        print("Lorenzo response: {} - {}", r.status_code, r.reason)
        return scan.id