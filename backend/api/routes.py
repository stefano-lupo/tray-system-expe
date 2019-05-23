import os
import base64
from uuid import uuid4
from typing import List, Dict
from flask import request, Response, jsonify, send_from_directory, send_file
import cv2 as cv
import json
import numpy as np

from core.config import UPLOAD_DIR
from . import app
from core.dao_models.detected_ingredient import DetectedIngredient
from core.dao_models.scan import Scan
from core.endpoints import Endpoint
from core.scan_request import ScanRequest
from core.dao_models.detection import Detection
from backend.database.daos.detected_ingredients_dao import DetectedIngredientsDao
from backend.database.daos.images_dao import ImagesDao
from backend.database.daos.scans_dao import ScansDao
from backend.detection.detector import Detector

from io import BytesIO
from PIL import Image

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


# @app.route("/static/image/<path:id>", methods=["GET"])
# def serve_image(id):
#     filename = images_dao.get_images([id])[0].path
#     print(filename)
#     print(UPLOAD_DIR)
#     return send_from_directory(UPLOAD_DIR, filename)

# @app.route('/image')
# def image():
#     img = cv.imread('raw.png')
#     data = cv.imencode('.png', img)[1].tobytes()
#     return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image/detections/<int:id>')
def image(id):
    MAX_HUE = 180
    SAT = 255
    VAL = 255
    images = images_dao.get_images()
    if len(images) == 0:
        print("No image for id %s " % id)
    image = images[0]
    filename = image.path
    img = cv.imread(os.path.join(UPLOAD_DIR, filename))
    detected_ingredients = images_dao.get_ingredients_in_image(id)
    for detected_ingredient in detected_ingredients:
        hue = max(0, min((detected_ingredient["ingredient_id"] + 1) * (MAX_HUE / 7), 255))
        hsv = np.uint8([[[hue, SAT, VAL]]])
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        color = tuple([int(i) for i in bgr[0][0]])
        detections = json.loads(detected_ingredient["detections"])
        for detection in detections:
            x = detection["x"]
            y = detection["y"]
            cv.rectangle(img, (x, y), (x + detection["width"]
            , y + detection["height"]), color, 2)
            # detect.segment.draw_segment(color_image, color, 1)
    return serve_pil_image(cv.cvtColor(img, cv.COLOR_BGR2RGB))

def serve_pil_image(pil_img):
    img_io = BytesIO()
    Image.fromarray(pil_img).save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
#
# @app.route('/images/<int:pid>.jpg')
# def get_image(pid):
#     # image_binary = cv.imread("./raw.jpg")
#     # response = make_response(image_binary)
#     # response.headers.set('Content-Type', 'image/jpeg')
#     # response.headers.set(
#     #     'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
#     # return response
#
#     return send_file(
#         BytesIO(cv.imread("./raw.jpg")),
#         mimetype='image/jpeg',
#         as_attachment=True,
#         attachment_filename='%s.jpg' % pid)