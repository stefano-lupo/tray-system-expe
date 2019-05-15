import os
from uuid import uuid4
from typing import List, Dict
from flask import request
import jsonpickle as jp
import json

from core.config import UPLOAD_DIR
from api import app
from core.dao_models.detected_ingredient import DetectedIngredient
from core.dao_models.scan import Scan
from core.endpoints import Endpoint
from core.scan_request import ScanRequest
from database.daos.detected_ingredients_dao import DetectedIngredientsDao
from database.daos.images_dao import ImagesDao
from database.daos.scans_dao import ScansDao
from detection.detector import Detector


images_dao: ImagesDao = ImagesDao()
scans_dao: ScansDao = ScansDao()
detected_ingredients_dao: DetectedIngredientsDao = DetectedIngredientsDao()

detector: Detector = Detector()


@app.route(Endpoint.SCAN.get_without_prefix(), methods=["POST"])
def scan_route():
    json = request.form['json']
    image = request.files['image']

    filename = os.path.join(UPLOAD_DIR, str(uuid4()) + ".jpg")
    image.save(filename)
    image_id = images_dao.insert_images([filename])

    scan_request = ScanRequest.from_request(json, filename)
    scan = Scan.from_scan_request(scan_request, image_id)
    scan.id = scans_dao.insert_scans([scan])

    detected_ingredients: List[DetectedIngredient] = detector.handle_scan(scan_request, scan.id)
    detected_ingredients_dao.insert_detected_ingredients(detected_ingredients)

    return "Scan successful"


@app.route(Endpoint.WASTE_BY_MENU_ITEM.get_without_prefix(), methods=["GET"])
def waste_by_menu_item_route() -> str:
    res: Dict = detected_ingredients_dao.get_waste_by_menu_item()
    return json.dumps(res)
