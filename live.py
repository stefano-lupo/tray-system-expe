import numpy as np
import cv2 as cv
import pyrealsense2 as rs

from time import sleep

from core.config import REALSENSE_WIDTH, REALSENSE_HEIGHT
from backend.detection.circle_detector import CircleDetector
from backend.detection.ingredient_detector import IngredientDetector

from keras.preprocessing import image

SAT = 255
VAL = 255
MAX_HUE = 180

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.z16, 30)
config.enable_stream(rs.stream.color, REALSENSE_WIDTH, REALSENSE_HEIGHT, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
    pipeline.wait_for_frames()

circle_detector: CircleDetector = CircleDetector()
ingredient_detector: IngredientDetector = IngredientDetector()
colorizer = rs.colorizer()
hole_filler = rs.hole_filling_filter()

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
    pipeline.wait_for_frames()

# img = image.load_img('test.jpg')
# y = image.img_to_array(img)
# y = np.expand_dims(y, axis=0)

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



    # if cv.waitKey(1) & 0xFF == ord(' '):
    segmented_circles = circle_detector.get_segmented_circles(color_image)
    skips = 0
    non_skips = 0
    for segmented_circle in segmented_circles:
        for segment in segmented_circle.segments:
            predictions = ingredient_detector.label(segment.get_segment_of_image(color_image))
            if predictions is None:
                # print("Had none")
                skips = skips + 1
                continue
            index = np.argmax(predictions[0])
            hue = max(0, min(index * (MAX_HUE / 7), 255))
            # print("Red: %s" % red)
            non_skips = non_skips + 1

            hsv = np.uint8([[[hue, SAT, VAL]]])
            bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
            color = tuple([int(i) for i in bgr[0][0]])
            segment.draw_segment(color_image_with_grid, colour=color, thickness=2, pad=1)
        # segments = segmented_circle.get_segments_of_image(color_image)
        # for segment in segments:
        #     prediction = np.where(ingredient_detector.label(segment) == 1)
        #     cv.rect(color_image_with_grid, segment.)
    # print("Had %s skips and %s non skips" % (skips, non_skips))

    cv.imshow("Depth", depth_image)
    cv.imshow("RGB", color_image_with_grid)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

