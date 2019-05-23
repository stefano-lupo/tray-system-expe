import os
import base64
from uuid import uuid4
from typing import List, Dict
from flask import request, jsonify, send_from_directory
import json

from core.config import UPLOAD_DIR
from . import app
from core.dao_models.detected_ingredient import DetectedIngredient
from core.dao_models.scan import Scan
from core.endpoints import Endpoint
from core.scan_request import ScanRequest
from backend.database.daos.detected_ingredients_dao import DetectedIngredientsDao
from backend.database.daos.images_dao import ImagesDao
from backend.database.daos.scans_dao import ScansDao
from backend.detection.detector import Detector


images_dao: ImagesDao = ImagesDao()
scans_dao: ScansDao = ScansDao()
detected_ingredients_dao: DetectedIngredientsDao = DetectedIngredientsDao()

detector: Detector = Detector()


@app.route(Endpoint.SCAN.get_without_prefix(), methods=["POST"])
def scan_route():
    json = request.form['json']
    image = request.files['image']

    filename = base64.urlsafe_b64encode(uuid4().bytes)
    filename = filename.strip(b'=').decode('ascii')
    filename = str(filename) + ".jpg"

    full_filename = os.path.join(UPLOAD_DIR, filename)
    image.save(full_filename)
    image_id = images_dao.insert_images([filename])

    scan_request = ScanRequest.from_request(json, full_filename)
    scan = Scan.from_scan_request(scan_request, image_id)
    scan.id = scans_dao.insert_scans([scan])

    detected_ingredients: List[DetectedIngredient] = detector.handle_scan(scan_request, scan.id)
    detected_ingredients_dao.insert_detected_ingredients(detected_ingredients)

    return "Scan successful"


@app.route(Endpoint.WASTE_BY_MENU_ITEM.get_without_prefix(), methods=["GET"])
def waste_by_menu_item_route() -> str:
    res: Dict = detected_ingredients_dao.get_waste_by_menu_item()
    return jsonify(res)

@app.route(Endpoint.WASTE_BY_INGREDIENT.get_without_prefix(), methods=["GET"])
def waste_by_ingredient() -> str:
    res: Dict = detected_ingredients_dao.get_waste_by_ingredient()
    return jsonify(res)

@app.route(Endpoint.WASTE_PER_HOUR.get_without_prefix(), methods=["GET"])
def waste_per_hour() -> str:
    return jsonify(detected_ingredients_dao.get_waste_per_hour())

@app.route(Endpoint.RECENT_IMAGES.get_without_prefix(), methods=["GET"])
def get_recent_images():
    images = images_dao.get_images()
    return jsonify([i.get_as_json() for i in images])

print(Endpoint.IMAGE.get_without_prefix())

@app.route("/image/<path:id>", methods=["GET"])
def serve_image(id):
    filename = images_dao.get_images([id])[0].path
    print(filename)
    print(UPLOAD_DIR)
    return send_from_directory(UPLOAD_DIR, filename)