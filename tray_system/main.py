import jsonpickle as jp

from core.scan import Scan
from data_pusher import DataPusher


if __name__ == "__main__":
    scan: Scan = Scan(1, 1, [], [], 1)
    dataPusher: DataPusher = DataPusher()
    dataPusher.push_scan(scan)