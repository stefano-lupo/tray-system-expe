import cv2 as cv
import numpy as np

from collections import defaultdict
from typing import List, Dict

from core.config import DEPTH_UNIT_SCALE_FACTOR, PLATE_DIAMETER_MM
from .circle_detector import CircleDetector
from .ingredient_detector import IngredientDetector
from .segmented_circle import SegmentedCircle, Segment

from core.scan_request import ScanRequest
from core.dao_models.ingredient import Ingredient
from core.dao_models.detection import Detection
from core.dao_models.detected_ingredient import DetectedIngredient

EMPTY_PLATE_ID = 3

def calculate_mass(depth_map: np.ndarray, segment: Segment, mm_per_pixel: int) -> int:
    # mass = int(np.average(segment.get_segment_of(depth_map)) * DEPTH_UNIT_SCALE_FACTOR * segment.get_area())
    area = segment.get_area() * (mm_per_pixel ** 2)
    average_depth = int(np.average(segment.get_segment_of(depth_map)))
    # masses.append(mass)
    # return mass
    return average_depth
    # return int(np.average(segment.get_segment_of(depth_map)))

class Detector:
    def __init__(self):
        self.circle_detector = CircleDetector()
        self.ingredient_detector = IngredientDetector()

    def run_detection(self, scan_request: ScanRequest, scan_id: int) -> List[DetectedIngredient]:
        image = np.array(scan_request.image)

        depth_map = np.array(scan_request.depth_map)
        segmented_circles: List[SegmentedCircle] = self.circle_detector.get_segmented_circles(image)
        if len(segmented_circles) > 1:
            print("WARN: Found more than one circle")

        detected_ingredients: Dict[Ingredient, List[Detection]] = defaultdict(list)
        for segmented_circle in segmented_circles:
            # segmented_circle.draw(image)

            radius_pixels = segmented_circle.circle.r
            mm_per_pixel = (PLATE_DIAMETER_MM / 2) / radius_pixels
            max_depth_in_circle = segmented_circle.get_max_value_in_circle(depth_map)
            print("Max depth in circle was %d" % max_depth_in_circle)
            print("mm per pixel was %d" % mm_per_pixel)

            # Mutating datastructures here
            self.ingredient_detector.transform_image_for_classification(image)
            depth_map = max_depth_in_circle - depth_map

            for segment in segmented_circle.segments:
                ingredient = self.ingredient_detector.label(segment.get_segment_of(image))
                if ingredient is None or ingredient is EMPTY_PLATE_ID:
                    continue
                mass = calculate_mass(depth_map, segment, mm_per_pixel)
                print(mass)
                detection: Detection = Detection(segment.x1, segment.y1, mass)
                detected_ingredients[ingredient].append(detection)

        results = [DetectedIngredient(scan_id, k.id, v) for (k, v) in detected_ingredients.items()]
        print("Found {} detected ingredients: {}".format(len(results), [r.ingredient_id for r in results]))
        return results


if __name__ == "__main__":
    img: np.ndarray = cv.imread("../../test.jpg")
    depth_map = 500 * np.random.rand(img.shape[0], img.shape[1])
    scan_req = ScanRequest(img, depth_map, 1, 1)

    from tray_system.data_pusher import DataPusher
    dp = DataPusher()
    dp.push_scan(scan_req)
    # detector.run_detection(scan_req)