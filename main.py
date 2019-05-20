import os
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
import shutil

from backend.detection.circle_detector import CircleDetector
from backend.detection.segmented_circle import Segment, SegmentedCircle
from core.config import IMAGE_SEGMENT_SIZE_PX

WIDTH = 640
HEIGHT = 480
INGREDIENT = "pasta"
TRAINING_IMAGE_DIR = "./training_images"
ingredient_dir = os.path.join(TRAINING_IMAGE_DIR, INGREDIENT)

EVAL_SPLIT_SIZE = 0.2

OUTPUT_DIR = "split_training_images_{}".format(IMAGE_SEGMENT_SIZE_PX)


def sample_image(rgbImage: np.ndarray, segmented_circle: SegmentedCircle, target_dir: str, start_id: int):
    samples: np.ndarray = segmented_circle.get_segments_of_image(rgbImage)
    for i, sample in enumerate(samples):
        name = os.path.join(target_dir, "{}.jpg".format(start_id + i))
        print("Writing %s" % name)
        cv.imwrite(name, sample)
    print(len(samples))



def generate_samples():
    circle_detector: CircleDetector = CircleDetector()
    for ingredient_dir in os.listdir(TRAINING_IMAGE_DIR):
        full_ingredient_dir = os.path.join(TRAINING_IMAGE_DIR, ingredient_dir)
        skip = 0
        for image_dir in os.listdir(full_ingredient_dir):
            full_image_dir = os.path.join(full_ingredient_dir, image_dir)
            img = cv.imread(os.path.join(full_image_dir, "raw.jpg"))

            target_dir = os.path.join(OUTPUT_DIR, ingredient_dir)
            print("Using target dir %s" % target_dir)

            os.makedirs(target_dir, exist_ok=True)
            segmented_circles = circle_detector.get_segmented_circles(img)
            [sample_image(img, sc, target_dir, skip) for sc in segmented_circles]
            skip = skip + len(segmented_circles[0].segments)

def train_test_split():
    train_dir = os.path.join(OUTPUT_DIR, "train")
    test_dir = os.path.join(OUTPUT_DIR, "test")
    if os.path.exists(train_dir):
        shutil.rmtree(train_dir)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    ingredient_dirs = os.listdir(OUTPUT_DIR)
    os.mkdir(train_dir)
    os.mkdir(test_dir)
    for ingredient_dir in ingredient_dirs:
        os.mkdir(os.path.join(train_dir, ingredient_dir))
        os.mkdir(os.path.join(test_dir, ingredient_dir))
        images = os.listdir(os.path.join(OUTPUT_DIR, ingredient_dir))
        np.random.shuffle(images)
        test_index = int(len(images) * EVAL_SPLIT_SIZE)
        test = images[:test_index]
        train = images[test_index:]
        for t in test:
            name = os.path.join(OUTPUT_DIR, ingredient_dir, t)
            target = os.path.join(test_dir, ingredient_dir, t)
            print(name)
            print(target)
            os.rename(name, target)
        for t in train:
            name = os.path.join(OUTPUT_DIR, ingredient_dir, t)
            os.rename(name, os.path.join(train_dir, ingredient_dir, t))




def get_images(next_id: int = 0):
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
        next_id = 0 if len(dirs) == 0 else max(dirs) + 1

    # generate_samples()
    train_test_split()

    # print("Starting for %s with next_id = %d" % (INGREDIENT, next_id))
    # get_images(next_id)
