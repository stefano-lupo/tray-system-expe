import json
import os
from io import BytesIO
from typing import Dict

import cv2 as cv
import numpy as np
from PIL import Image
from flask import request, jsonify, send_file, redirect, abort

from backend.database.daos.detected_ingredients_dao import DetectedIngredientsDao
from backend.database.daos.images_dao import ImagesDao
from backend.database.daos.master_dao import MasterDao
from backend.database.daos.scans_dao import ScansDao
# from backend.detection.detector import Detector
from backend.detection.scan_handler import ScanHandler
from core.config import UPLOAD_DIR
from core.endpoints import Endpoint
from . import app

images_dao: ImagesDao = ImagesDao()
scans_dao: ScansDao = ScansDao()
detected_ingredients_dao: DetectedIngredientsDao = DetectedIngredientsDao()
master_dao: MasterDao = MasterDao()

# detector: Detector = Detector()
# scan_handler: ScanHandler = ScanHandler()


@app.route(Endpoint.SCAN.get_without_prefix(), methods=["POST"])
def scan_route():
    json = request.form['json']
    image = request.files['image']

    # return scan_handler.handle_endpoint_scan(image, json)

    # filename = base64.urlsafe_b64encode(uuid4().bytes)
    # filename = filename.strip(b'=').decode('ascii')
    # filename = str(filename) + ".jpg"

    # full_filename = os.path.join(UPLOAD_DIR, filename)
    # image.save(full_filename)
    # image_id = images_dao.insert_images([filename])

    # scan_request = ScanRequest.from_request(json, full_filename)
    # scan = Scan.from_scan_request(scan_request, image_id)
    # scan.id = scans_dao.insert_scans([scan])

    # detected_ingredients: List[DetectedIngredient] = detector.run_detection(scan_request, scan.id)
    # detected_ingredients_dao.insert_detected_ingredients(detected_ingredients)

    # return scan.id


@app.route(Endpoint.WASTE_BY_MENU_ITEM.get_without_prefix(), methods=["GET"])
def waste_by_menu_item_route() -> str:
    res: Dict = master_dao.get_waste_by_menu_item()
    return jsonify(res)


@app.route(Endpoint.WASTE_BY_INGREDIENT.get_without_prefix(), methods=["GET"])
def waste_by_ingredient() -> str:
    res: Dict = master_dao.get_waste_by_ingredient()
    return jsonify(res)


@app.route(Endpoint.WASTE_PER_HOUR.get_without_prefix(), methods=["GET"])
def waste_per_hour() -> str:
    return jsonify(master_dao.get_waste_per_hour())


@app.route(Endpoint.RECENT_SCANS.get_without_prefix(), methods=["GET"])
def get_recent_scans():
    mqrs_by_id = master_dao.get_recent()
    return jsonify({k: swd.get_as_dict() for (k, swd) in mqrs_by_id.items()})

@app.route(Endpoint.DETECTIONS.get_without_prefix(), methods=["GET"])
def get_detection_by_scan_id():
    scan_id = request.args.get('scan_id')
    if scan_id is None:
        abort(400, "A scan id must be provided")
    scan_id = int(scan_id)
    as_dict = {k: v.get_as_dict() for (k, v) in master_dao.get_detections_by_scan_id([scan_id]).items()}
    return jsonify(as_dict)


@app.route(Endpoint.IMAGE.get_without_prefix(), methods=["GET"])
def get_image():
    image_id = request.args.get('image_id')
    scan_id = request.args.get('scan_id')

    if not image_id and not scan_id:
        abort(400, "Either an image_id or a scan_id must be provided as query params")

    file_name = images_dao.get_path(image_id, scan_id)
    if file_name is None:
        abort(404, "No image found for image_id {}, scan_id {}".format(image_id, scan_id))
    return redirect("/static/images/{}".format(file_name))


@app.route(Endpoint.DETECTIONS_IMAGE.get_without_prefix(), methods=["GET"])
def get_image_with_detections():
    scan_id = request.args.get('scan_id')
    MAX_HUE = 180
    SAT = 255
    VAL = 255

    images = images_dao.get_image_by_scan_id(scan_id)
    if len(images) == 0:
        abort(404, "No image for scan_id %s " % scan_id)

    image = images[0]
    filename = image["path"]
    img = cv.imread(os.path.join(UPLOAD_DIR, filename))
    detected_ingredients = images_dao.get_ingredients_in_image(image["image_id"])
    for detected_ingredient in detected_ingredients:
        # # hue = max(0, min((detected_ingredient["ingredient_id"] + 1) * (MAX_HUE / 7), 255))
        # hue = max(0, min((detected_ingredient["mass"])))
        # hsv = np.uint8([[[hue, SAT, VAL]]])
        # bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        # color = tuple([int(i) for i in bgr[0][0]])
        detections = json.loads(detected_ingredient["detections"])
        for detection in detections:
            x = detection["x"]
            y = detection["y"]
            mass = detection["mass"]
            print(mass)
            hue = mass * MAX_HUE / 1100
            hsv = np.uint8([[[hue, SAT, VAL]]])
            bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
            color = tuple([int(i) for i in bgr[0][0]])
            cv.rectangle(img, (x, y), (x + detection["width"], y + detection["height"]), color, 2)
            # detect.segment.draw_segment(color_image, color, 1)
    return serve_pil_image(cv.cvtColor(img, cv.COLOR_BGR2RGB))


def serve_pil_image(pil_img):
    img_io = BytesIO()
    Image.fromarray(pil_img).save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

