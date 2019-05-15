import cv2 as cv
import numpy as np

from collections import defaultdict
from typing import List, Dict

from config import DEPTH_UNIT_SCALE_FACTOR
from circle_detector import CircleDetector
from ingredient_detector import IngredientDetector
from segmented_circle import SegmentedCircle, Segment

from core.scan_request import ScanRequest
from core.dao_models.ingredient import Ingredient
from core.dao_models.detection import Detection
from core.dao_models.detected_ingredient import DetectedIngredient


def calculate_mass(depth_map: np.ndarray, segment: Segment) -> float:
    return np.average(segment.get_segment_of(depth_map)) * DEPTH_UNIT_SCALE_FACTOR * segment.get_area()


class Detector:
    def __init__(self):
        self.circle_detector = CircleDetector()
        self.ingredient_detector = IngredientDetector()

    def handle_scan(self, scan_request: ScanRequest, scan_id: int) -> List[DetectedIngredient]:
        image = np.array(scan_request.image)

        depth_map = np.array(scan_request.depth_map)
        segmented_circles: List[SegmentedCircle] = self.circle_detector.get_segmented_circles(image)

        detected_ingredients: Dict[Ingredient, List[Detection]] = defaultdict(list)
        for segmented_circle in segmented_circles:
            segmented_circle.draw(image)
            for segment in segmented_circle.segments:
                ingredient = self.ingredient_detector.label(segment.get_segment_of(image))
                if ingredient is None:
                    continue
                detection: Detection = Detection(segment.x1, segment.y1, calculate_mass(depth_map, segment))
                detected_ingredients[ingredient].append(detection)

        return [DetectedIngredient(scan_id, k.id, v) for (k, v) in detected_ingredients.items()]


if __name__ == "__main__":
    img: np.ndarray = cv.imread("../../test.jpg")
    depth_map = np.random.rand(img.shape[0], img.shape[1])
    detector = Detector()
    scan_req = ScanRequest(img, depth_map, 1, 1)

    from tray_system.data_pusher import DataPusher
    dp = DataPusher()
    dp.push_scan(scan_req)
    # detector.handle_scan(scan_req)