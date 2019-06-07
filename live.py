import numpy as np
import cv2 as cv
import pyrealsense2 as rs
import os
from collections import defaultdict
from time import sleep
import json

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
# INGREDIENTS = ["broccoli", "chicken", "green_beans", "lettuce", "pasta", "rice", "tomato"]
INGREDIENTS = ["broccoli", "chicken", "cutlery", "empty", "green_beans", "lettuce", "pasta", "rice", "tomato"]


def check_for_key():
    if cv.waitKey(1) & 0xFF == ord('q'):
        return True

    return False

def show_image(img):
    if img is None:
        print("none image")
        return
    cv.imshow("img", img)
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def format_predictions(predictions):
    zipped = dict(zip(INGREDIENTS, predictions))
    zipped = {k: v for (k, v) in zipped.items() if v > 0.01}
    return {k: "{0:.2f}".format(v) for  (k,v) in zipped.items()}


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
                # cv.imwrite("segments/%d.jpg" % i, img_segment)
                # cv.imshow("segment", img_segment)
                # while True:
                #     key = cv.waitKey(1) & 0xFF
                #     if  key == ord('s'):
                #         cv.imwrite("small.jpg", img_segment)
                #         break
                #     elif key == ord(' '):
                #         break
                transformed = ingredient_detector.transform_image_for_classification(img_segment)
                ingredient = ingredient_detector.label(transformed)

                # print(format_predictions(predictions))
                # if ingredient is None or ingredient.name == "Empty":
                if ingredient is None or ingredient.name == "Cutlery" or ingredient.name == "Empty":
                    print("Had none")
                    all_predictions[ingredient] = all_predictions[ingredient] + 1
                    skips = skips + 1
                    continue

                # print("Detected: %s" % ingredient.name)

                hue = max(0, min((ingredient.id + 1) * (MAX_HUE / 9), 255))
                # print("Red: %s" % red)
                all_predictions[ingredient] = all_predictions[ingredient] + 1
                non_skips = non_skips + 1

                hsv = np.uint8([[[hue, SAT, VAL]]])
                bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
                color = tuple([int(i) for i in bgr[0][0]])
            except:
                print("Derp")
            segment.draw_segment(color_image, colour=color, thickness=2, pad=1)

    print({"None" if k is None else k.name: v for (k, v) in all_predictions.items()})
    #
    # advnc_mode = rs.rs400_advanced_mode(device)
    #
    # with open("profile.json") as f:
    #     res = json.load(f)
    #     # print(isinstance(, str))
    #     advnc_mode.load_json(json.dumps(res))edictions.items()})

def run_live(ingredient_detector):
    data_pusher = DataPusher()
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.bgr8, 30)

    align_to = rs.stream.color
    align = rs.align(align_to)

    # Start streaming
    profile = pipeline.start(config)
    device = profile.get_device()

    advnc_mode = rs.rs400_advanced_mode(device)

    with open("profile.json") as f:
        res = json.load(f)
        # print(isinstance(, str))
        advnc_mode.load_json(json.dumps(res))

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

        depth_image = np.asanyarray(colorizer.colorize(depth).get_data(), dtype=np.uint8)
        # depth_image = np.asanyarray(depth.get_data(), dtype=np.uint8)

        color_image = np.asanyarray(color.get_data(), dtype=np.uint8)
        color_image_with_overlay = np.copy(color_image)

        cv.imwrite("rgb.jpg", color_image)
        # cv.imwrite("depth.jpg", depth_image)

        process_colour_image(color_image_with_overlay, ingredient_detector)
        # circle_detector.draw_segmented_circle(color_image_with_overlay)

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


def test_image(ingredient_detector: IngredientDetector, img):
    if img is None:
        print("you are dumb")
        return
    process_colour_image(img, ingredient_detector)
    cv.imshow("Image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def load():
    depth = np.load("depth.txt.npy")
    colour = np.load("colour.txt.npy")

    depth = depth * 255.0/depth.max()
    # print(depth.shape)
    # print(colour.shape)

    cv.imshow("colour", colour)
    cv.imshow("depth", depth)
    while True:
        if check_for_key():
            break

def test_images(ingredient_detector):
    ingredients = os.listdir("split_training_images_cleaned_50/test")
    for ingredient in ingredients:
        print("Ingredient: %s" % ingredient)
        full_dir = os.path.join("split_training_images_cleaned_50/test", ingredient)
        file = os.path.join(full_dir, os.listdir(full_dir)[0])
        print("file")
        img = cv.imread(file)
        cv.imshow("Image", img)
        cv.waitKey(0)
        # test_image(ingredient_detector, img)
        transformed = ingredient_detector.transform_image_for_classification(img)

        # cv.destroyAllWindows()
        predictions = ingredient_detector.predict(transformed)[0]
        predictions = ["{0:.2f}".format(p) for p in predictions]
        print(predictions)

def small_test(ingredient_detector, dir):
    for img in os.listdir(dir):
        img = os.path.join(dir, img)
        print(img)
        img = cv.imread(img)

        if img is None:
            continue
        # img = img - 50
        show_image(img)

        transformed = ingredient_detector.transform_image_for_classification(img)

        # cv.destroyAllWindows()
        predictions = ingredient_detector.predict(transformed)[0]
        # predictions = ["{0:.2f}".format(p) for p in predictions]
        print(format_predictions(predictions))

def predict(ingredient_detector, img):
    transformed = ingredient_detector.transform_image_for_classification(img)
    predictions = ingredient_detector.predict(transformed)[0]
    # predictions = ["{0:.2f}".format(p) for p in predictions]
    print(format_predictions(predictions))


if __name__ == "__main__":
    ingredient_detector: IngredientDetector = IngredientDetector()
    # img =  cv.imread("segments/109.jpg")
    # show_image(img)
    # predict(ingredient_detector, img)
    run_live(ingredient_detector)
    # test_images(ingredient_detector)
    # test_image(ingredient_detector, cv.imread("split_training_images_cleaned_50/train/brocoli/1.jpg"))
    # small_test(ingredient_detector, "split_training_images_cleaned_50/test/empty")
    # load()


