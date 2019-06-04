import numpy as np

from typing import Dict

import requests
from requests.exceptions import HTTPError
import jsonpickle as jp

from core.scan_request import ScanRequest
from core.endpoints import Endpoint

MULTIPART_HEADER = {'Content-type': 'multipart/form-data'}

import cv2 as cv

class DataPusher:

    def __init__(self):
        pass

    def push_scan(self, scan_request: ScanRequest):
        _, img_encoded = cv.imencode('.jpg', scan_request.image)
        payload = {
            'json': (None, scan_request.get_json(), 'application/json'),
            'image': ("ignored.jpg", img_encoded),
        }

        resp = requests.post(Endpoint.SCAN.get(), files=payload)

        if resp.status_code == requests.codes.ok:
            print("Successfully pushed scan to server")
        else:
            print("Unable to push scan to server")
        
        # TODO: Return scan id
        return resp.data

    def post(self, endpoint: Endpoint, obj: Dict):
        try:
            response = requests.post(endpoint.get(), json=obj)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')
