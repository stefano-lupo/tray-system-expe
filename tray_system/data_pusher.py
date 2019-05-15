from typing import Dict

import requests
from requests.exceptions import HTTPError
import jsonpickle as jp

from core.scan import Scan
from core.endpoints import Endpoint

class DataPusher:

    def __init__(self):
        pass

    def push_scan(self, scan: Scan):
        self.post(Endpoint.SCAN, jp.encode(scan))

    def post(self, endpoint: Endpoint, obj: Dict):
        try:
            response = requests.post(endpoint.get(), json=obj)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')