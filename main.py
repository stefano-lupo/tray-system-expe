import os
import pyrealsense2 as rs
import numpy as np
import cv2 as cv

from backend.detection.circle_detector import CircleDetector
from backend.detection.segmented_circle import Segment, SegmentedCircle

WIDTH = 640
HEIGHT = 480
INGREDIENT = "pasta"
DIR = "./training_images"
ingredient_dir = os.path.join(DIR, INGREDIENT)


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, 30)
config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
    pipeline.wait_for_frames()

circle_detector: CircleDetector = CircleDetector()
colorizer = rs.colorizer()
hole_filler = rs.hole_filling_filter()

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
    pipeline.wait_for_frames()

def sample_image(rgbImage: np.ndarray, segmented_circle: SegmentedCircle, target_dir: str):
    samples: np.ndarray = segmented_circle.get_segments_of_image(rgbImage)
    for i, sample in enumerate(samples):
        name = os.path.join(target_dir, "{}.jpg".format(i))
        cv.imwrite(name, sample)
    print(len(samples))

def get_images(next_id: int = 0):
    while True:
        frames = pipeline.wait_for_frames(timeout_ms=5000)
        color = frames.get_color_frame()

        depth = frames.get_depth_frame()
        depth = hole_filler.process(depth)

        if not depth or not color:
            continue

        depth_image = np.asanyarray(colorizer.colorize(depth).get_data())
        color_image = np.asanyarray(color.get_data(), dtype=np.uint8)

        color_image_with_grid = np.copy(color_image)
        circle_detector.draw_segmented_circle(color_image_with_grid)

        cv.imshow("Depth", depth_image)
        cv.imshow("RGB", color_image_with_grid)

        if cv.waitKey(1) & 0xFF == ord(' '):
            target_dir = os.path.join(ingredient_dir, str(next_id))
            if os.path.exists(target_dir):
                raise ValueError("Directory %s exists" % target_dir)
            else:
                os.mkdir(target_dir)
            name = os.path.join(target_dir, "raw.jpg")
            print("Capture %s " % name)

            cv.imwrite(name, color_image)
            # [sample_image(color_image, sc, target_dir) for sc in circle_detector.get_segmented_circles(color_image)]
            next_id = next_id + 1

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    next_id = 0
    if not os.path.exists(ingredient_dir):
        os.mkdir(ingredient_dir)
    else:
        dirs = os.listdir(ingredient_dir)
        dirs = [int(d) for d in dirs]
        print(dirs)
        next_id = 0 if len(dirs) == 0 else max(dirs) + 1

    print("Starting for %s with next_id = %d" % (INGREDIENT, next_id))
    get_images(next_id)
