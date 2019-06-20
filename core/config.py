# API_HOST = "10.42.0.1"
# API_HOST = "192.168.1.155"
# API_HOST = "172.20.10.2"
# API_HOST = "localhost"
API_HOST = "0.0.0.0"
# API_HOST = "192.168.5.14"
API_PORT = 8080
LORENZO_URL = "https://magna-tron.appspot.com/api/v0.1/participants"
UPLOAD_DIR="backend/api/static/images/"
ASSETS_DIR="assets/"

DB_CONFIG = {
    "host": "localhost",
    "user": "tray_system",
    "passwd": "tray_system",
    "database": "tray_system"
}

IMAGE_SEGMENT_SIZE_PX = 50
NUM_CLASSES = 9
SMALL_MODEL = "models/small_cnn.h5"
RES_NET_MODEL = "models/res_net_50.h5"
CUSTOM_MODEL = "models/custom_90_perc.h5"
FINAL_MODEL = "models/expe_model.h5"

CIRCLE_DETECT_MIN_RADIUS = 50
CIRCLE_DETECT_MIN_DISTANCE_BETWEEN_CENTERS = 50
CIRCLE_DETECT_PADDING_BOXES = 1
PLATE_DIAMETER_MM = 267

DEPTH_UNIT_SCALE_FACTOR = 1
REALSENSE_WIDTH = 1280
REALSENSE_HEIGHT = 720

WEBSOCKET_PORT = 8081
WEBSOCKET_BASE_URL = API_HOST