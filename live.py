import numpy as np
import cv2 as cv
import pyrealsense2 as rs
import os

from time import sleep

from core.config import REALSENSE_WIDTH, REALSENSE_HEIGHT
from backend.detection.detector import Detector
from backend.detection.circle_detector import CircleDetector
from backend.detection.ingredient_detector import IngredientDetector

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

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

            predictions = ingredient_detector.label(segment.get_segment_of_image(color_image))
            # print(format_predictions(predictions))
            if predictions is None:
                # print("Had none")
                all_predictions.append(predictions)
                skips = skips + 1
                continue
            index = np.argmax(predictions[0])
            hue = max(0, min((index + 1) * (MAX_HUE / 7), 255))
            # print("Red: %s" % red)
            non_skips = non_skips + 1

            hsv = np.uint8([[[hue, SAT, VAL]]])
            bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
            color = tuple([int(i) for i in bgr[0][0]])
            segment.draw_segment(color_image, colour=color, thickness=2, pad=1)



def run_live(ingredient_detector):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    colorizer = rs.colorizer()
    hole_filler = rs.hole_filling_filter()

    # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(5):
        pipeline.wait_for_frames()

    while True:
        frames = pipeline.wait_for_frames(timeout_ms=5000)
        color = frames.get_color_frame()

        depth = frames.get_depth_frame()
        depth = hole_filler.process(depth)

        if not depth or not color:
            continue

        depth_image = np.asanyarray(colorizer.colorize(depth).get_data())
        color_image = np.asanyarray(color.get_data(), dtype=np.uint8)

        circle_detector.draw_segmented_circle(color_image)

        process_colour_image(color_image, ingredient_detector)
        check_for_key()

        cv.imshow("Depth", depth_image)
        cv.imshow("RGB", color_image)
        sleep(1)


def test_image(ingredient_detector: IngredientDetector):
    img = cv.imread("training_images/lettuce/1/raw.jpg")
    process_colour_image(img, ingredient_detector)
    cv.imshow("Image", img)
    while True:
        if check_for_key():
            break


if __name__ == "__main__":
    ingredient_detector: IngredientDetector = IngredientDetector()
    run_live(ingredient_detector)
    # test_image(ingredient_detector)


