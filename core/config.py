API_PORT = 8080
UPLOAD_DIR="images/"
ASSETS_DIR="assets/"

DB_CONFIG = {
    "host": "localhost",
    "user": "tray_system",
    "passwd": "tray_system",
    "database": "tray_system"
}

IMAGE_SEGMENT_SIZE_PX = 32
NUM_CLASSES = 7
SMALL_MODEL = "models/small_cnn.h5"
RES_NET_MODEL = "models/res_net_32.h5"

CIRCLE_DETECT_MIN_RADIUS = 100
CIRCLE_DETECT_MIN_DISTANCE_BETWEEN_CENTERS = 100
CIRCLE_DETECT_PADDING_BOXES = 1

DEPTH_UNIT_SCALE_FACTOR = 1
REALSENSE_WIDTH = 640
REALSENSE_HEIGHT = 480
