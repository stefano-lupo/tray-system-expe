import pyrealsense2 as rs
import json

from core.config import REALSENSE_HEIGHT, REALSENSE_WIDTH

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.z16, 30)
config.enable_stream(rs.stream.color, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.bgr8, 30)
colorizer = rs.colorizer()
hole_filler = rs.hole_filling_filter()
profile = pipeline.start(config)
device = profile.get_device()

advnc_mode = rs.rs400_advanced_mode(device)

with open("profile.json") as f:
    res = json.load(f)
    # print(isinstance(, str))
    advnc_mode.load_json(json.dumps(res))

if __name__ == "__main__":
    print("h")