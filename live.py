import numpy as np
import cv2 as cv
import pyrealsense2 as rs
import os

from time import sleep

from core.config import REALSENSE_WIDTH, REALSENSE_HEIGHT
from core.scan_request import ScanRequest
from backend.detection.detector import Detector
from backend.detection.circle_detector import CircleDetector
from backend.detection.ingredient_detector import IngredientDetector
from tray_system.data_pusher import DataPusher

SAT = 255
VAL = 255
MAX_HUE = 180

circle_detector: CircleDetector = CircleDetector()
detector: Detector = Detector()
INGREDIENTS = ["broccoli", "chicken", "green_beans", "lettuce", "pasta", "rice", "tomato"]


def check_for_key():
    if cv.waitKey(1) & 0xFF == ord('q'):
        return True

    return False

def format_predictions(predictions):
    as_strings = ["{0:.2f}".format(p) for p in predictions[0]]
    return dict(zip(INGREDIENTS, as_strings))


def process_colour_image(color_image, ingredient_detector):
    segmented_circles = circle_detector.get_segmented_circles(color_image)
    skips = 0
    non_skips = 0
    all_predictions = []
    for segmented_circle in segmented_circles:
        for segment in segmented_circle.segments:
            # cv.imshow("segment", segment.get_segment_of_image(color_image))
            # while True:
            #     if cv.waitKey(1) & 0xFF == ord('q'):
            #         break

            ingredient = ingredient_detector.label(segment.get_segment_of_image(color_image))
            # print(format_predictions(predictions))
            if ingredient is None:
                # print("Had none")
                all_predictions.append(ingredient)
                skips = skips + 1
                continue

            hue = max(0, min((ingredient.id + 1) * (MAX_HUE / 7), 255))
            # print("Red: %s" % red)
            non_skips = non_skips + 1

            hsv = np.uint8([[[hue, SAT, VAL]]])
            bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
            color = tuple([int(i) for i in bgr[0][0]])
            segment.draw_segment(color_image, colour=color, thickness=2, pad=1)



def run_live(ingredient_detector):
    data_pusher = DataPusher()
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.bgr8, 30)

    align_to = rs.stream.color
    align = rs.align(align_to)

    # Start streaming
    pipeline.start(config)

    colorizer = rs.colorizer()
    hole_filler = rs.hole_filling_filter()

    # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(5):
        pipeline.wait_for_frames()

    while True:
        frames = pipeline.wait_for_frames(timeout_ms=5000)
        aligned_frames = align.process(frames)

        color = aligned_frames.get_color_frame()
        depth = aligned_frames.get_depth_frame()
        depth = hole_filler.process(depth)
        # depth2 = depth.get_distance(100, 100)
        # print(depth2)

        if not depth or not color:
            continue

        depth_frame_data = np.asanyarray(depth.get_data())
        color_frame_data = np.asanyarray(color.get_data())

        # depth_image = np.asanyarray(colorizer.colorize(depth).get_data(), dtype=np.uint8)
        depth_image = np.asanyarray(depth.get_data(), dtype=np.uint8)

        color_image = np.asanyarray(color.get_data(), dtype=np.uint8)
        color_image_with_overlay = np.copy(color_image)

        # cv.imwrite("rgb.jpg", color_image)
        # cv.imwrite("depth.jpg", depth_image)

        process_colour_image(color_image_with_overlay, ingredient_detector)
        circle_detector.draw_segmented_circle(color_image_with_overlay)

        if cv.waitKey(1) & 0xFF == ord(' '):
            # np.save("colour.txt", color_image)
            # np.save("depth.txt", np.asanyarray(depth.get_data(), dtype=np.uint8))
            # r = color_image[:, :, 0]
            # g = color_image[:, :, 1]
            # b = color_image[:, :, 2]
            # np.savetxt("colour-r.txt", r)
            # np.savetxt("colour-g.txt", g)
            # np.savetxt("colour-b.txt", b)
            # np.savetxt("depth.txt", np.asanyarray(depth.get_data(), dtype=np.uint8))
            scan_request = ScanRequest(color_frame_data, depth_frame_data, 1, 1)
            data_pusher.push_scan(scan_request)

        check_for_key()

        cv.imshow("Depth", depth_image)
        cv.imshow("RGB", color_image_with_overlay)
        sleep(0.2)
        # return


def test_image(ingredient_detector: IngredientDetector):
    img = cv.imread("training_images/lettuce/1/raw.jpg")
    process_colour_image(img, ingredient_detector)
    cv.imshow("Image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def load():
    depth = np.load("depth.txt.npy")
    colour = np.load("colour.txt.npy")

    depth = depth * 255.0/depth.max()
    print(depth.shape)
    print(colour.shape)

    cv.imshow("colour", colour)
    cv.imshow("depth", depth)
    while True:
        if check_for_key():
            break

if __name__ == "__main__":
    ingredient_detector: IngredientDetector = IngredientDetector()
    run_live(ingredient_detector)
    # test_image(ingredient_detector)
    # load()


