import jsonpickle as jp

from flask import request
from typing import List

from api import app
from core.endpoints import Endpoint
from core.scan_request import ScanRequest
from detection import detector



@app.route(Endpoint.SCAN.get_without_prefix(), methods=["POST"])
def scan_route():
    # print(request.json())
    scan_request: ScanRequest = jp.decode(request.json)
    # detector.handle_scan(scan_request)
    return "hello"


