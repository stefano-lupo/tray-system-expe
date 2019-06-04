import pyrealsense2 as rs
import numpy as np

from core.config import REALSENSE_WIDTH, REALSENSE_HEIGHT


class RealSenseCapturer:

    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.bgr8, 30)
        self.colorizer = rs.colorizer()
        self.hole_filler = rs.hole_filling_filter()
        self.profile = self.pipeline.start(config)

        # Skip 5 first frames to give the Auto-Exposure time to adjust
        for x in range(5):
            self.pipeline.wait_for_frames()

    def capture(self, hole_fill=True):
        frames = self.pipeline.wait_for_frames(timeout_ms=5000)
        color = frames.get_color_frame()
        depth = frames.get_depth_frame()

        if hole_fill:
            depth = self.hole_filler.process(depth)

        if not depth or not color:
            print("Had null depth or color!")
            return

        depth_image = np.asanyarray(depth.get_data(), dtype=np.uint8)
        color_image = np.asanyarray(color.get_data(), dtype=np.uint8)
        
        depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()
        depth_image = depth_image * depth_scale

        return color_image, depth_image
        
