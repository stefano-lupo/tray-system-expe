import cv2 as cv
import numpy as np

from typing import Tuple, List, Dict

from .circle import Circle

import cv2 as cv
class Segment:

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_segment_of(self, arr: np.ndarray) -> np.ndarray:
        return arr[self.y1:self.y2, self.x1:self.x2]

    def get_area(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    def get_segment_of_image(self, image: np.ndarray) -> np.ndarray:
        pixels = image[self.y1:self.y2, self.x1: self.x2, :]
        # print(pixels.shape)
        # cv.imshow("tmp", pixels)
        # cv.waitKey(1)
        return pixels

    def draw_segment(self, image, colour=(125, 100, 0), thickness=0, pad=0):
        cv.rectangle(image, (self.x1 + pad, self.y1 + pad), (self.x2 - pad, self.y2 - pad), colour, thickness)


class SegmentedCircle:

    def __init__(self, circle: Circle):
        self.circle = circle
        self.segments: List[Segment] = []

    def add_segment(self, segment:Segment):
        self.segments.append(segment)

    def get_segments_of_image(self, image):
        return [s.get_segment_of_image(image) for s in self.segments]
    
    def get_max_value_in_circle(self, depth_image):
        segment_pixels = self.get_segments_of_image(depth_image)
        max_value = np.max([np.max(s) for s in segment_pixels])
        return max_value

    def draw(self, image: np.ndarray):
        cv.circle(image, (self.circle.x, self.circle.y), self.circle.r, (0, 255, 0), 2)
        for segment in self.segments:
            segment.draw_segment(image)