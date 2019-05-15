import jsonpickle as jp
from flask import request

from api import app
from core.endpoints import Endpoint
from core.scan import Scan


@app.route(Endpoint.SCAN.get_without_prefix(), methods=["POST"])
def scan_route():
    # print(request.json())
    scan: Scan = jp.decode(request.json)
    return "hello"