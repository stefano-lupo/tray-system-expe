##################################
# Shows a live feed from the camera
# with detections overlayed
##################################

from collections import defaultdict
from time import sleep

import cv2 as cv
import numpy as np
import pyrealsense2 as rs

from backend.detection.circle_detector import CircleDetector
from backend.detection.detector import Detector
from backend.detection.ingredient_detector import IngredientDetector
from core.config import REALSENSE_WIDTH, REALSENSE_HEIGHT, NUM_CLASSES
from core.scan_request import ScanRequest
from tray_system.data_pusher import DataPusher

SAT = 255
VAL = 255
MAX_HUE = 180

circle_detector: CircleDetector = CircleDetector()
detector: Detector = Detector()
INGREDIENTS = ["broccoli", "chicken", "cutlery", "empty", "green_beans", "lettuce", "pasta", "rice", "tomato"]


def check_for_key():
    if cv.waitKey(1) & 0xFF == ord('q'):
        return True

    return False


def process_colour_image(color_image, ingredient_detector):
    segmented_circles = circle_detector.get_segmented_circles(color_image)
    skips = 0
    non_skips = 0
    all_predictions = defaultdict(int)
    for segmented_circle in segmented_circles:
        for i, segment in enumerate(segmented_circle.segments):
            try:
                img_segment = segment.get_segment_of_image(color_image)
                if segment is None:
                    print("None segment")
                    continue

                transformed = ingredient_detector.transform_image_for_classification(img_segment)
                ingredient = ingredient_detector.label(transformed)

                if ingredient is None:
                    skips = skips + 1
                    print("Had None ingredient - Uh oh!")
                    continue

                non_skips = non_skips + 1
                all_predictions[ingredient] = all_predictions[ingredient] + 1

                # Skip cutlery or empties
                if ingredient.name == "Cutlery" or ingredient.name == "Empty":
                    continue

                # Compute hue angle - between 0 and 255 depending on class id
                hue = max(0, min((ingredient.id + 1) * (MAX_HUE / NUM_CLASSES), 255))

                # Convert HSV to BGR
                hsv = np.uint8([[[hue, SAT, VAL]]])
                bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
                color = tuple([int(i) for i in bgr[0][0]])
            except:
                print("Uncaught exception processing color image - Oh noes!")
                continue

            segment.draw_segment(color_image, colour=color, thickness=2, pad=1)

    print({"None" if k is None else k.name: v for (k, v) in all_predictions.items()})


def run_live(ingredient_detector):
    data_pusher = DataPusher()
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.bgr8, 30)

    # Since RGB camera and depth sensors aren't physically aligned, align them here
    align_to = rs.stream.color
    align = rs.align(align_to)

    # Start streaming
    profile = pipeline.start(config)
    device = profile.get_device()

    # Optionally load a camera profile
    # advnc_mode = rs.rs400_advanced_mode(device)
    # with open("profile.json") as f:
    #     res = json.load(f)
    #     print(isinstance(, str))
    #     advnc_mode.load_json(json.dumps(res))

    colorizer = rs.colorizer()                  # Represent depth map as colour
    hole_filler = rs.hole_filling_filter()      # Fill gaps in depth map

    # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(5):
        pipeline.wait_for_frames()

    # Poll camera
    while True:
        frames = pipeline.wait_for_frames(timeout_ms=5000)
        aligned_frames = align.process(frames)

        color = aligned_frames.get_color_frame()
        depth = aligned_frames.get_depth_frame()
        depth = hole_filler.process(depth)

        if not depth or not color:
            continue

        # Keep these as separate copies untouched to use incase we actually submit a snapshot
        # Subsequent copies of this data will be messed with for visualization
        depth_frame_data = np.asanyarray(depth.get_data())
        color_frame_data = np.asanyarray(color.get_data())

        depth_image_colourized = np.asanyarray(colorizer.colorize(depth).get_data(), dtype=np.uint8)
        # depth_image = np.asanyarray(depth.get_data(), dtype=np.uint8)

        # This will be overlayed with a grid
        color_image_with_overlay = np.copy(np.asanyarray(color.get_data(), dtype=np.uint8))
        process_colour_image(color_image_with_overlay, ingredient_detector)

        # circle_detector.draw_segmented_circle(color_image_with_overlay)

        # Hit space to actually record the snapshot and send it to the DB
        if cv.waitKey(1) & 0xFF == ord(' '):
            menu_item_id = 1
            user_id = 1
            scan_request = ScanRequest(color_frame_data, depth_frame_data, menu_item_id, user_id)
            data_pusher.push_scan(scan_request)

        check_for_key()

        depth = "Depth"
        rgb = "RGB"

        cv.namedWindow(depth, cv.WINDOW_NORMAL)
        cv.resizeWindow(depth, 640, 360)
        cv.imshow(depth, depth_image_colourized)

        cv.namedWindow(rgb, cv.WINDOW_NORMAL)
        cv.resizeWindow(rgb, 640, 360)
        cv.imshow(rgb, color_image_with_overlay)

        # Slow frame rate down to not cause nuclear fusion in your CPU
        sleep(0.2)


if __name__ == "__main__":
    ingredient_detector: IngredientDetector = IngredientDetector()
    run_live(ingredient_detector)
