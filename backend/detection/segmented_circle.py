import cv2 as cv
import numpy as np

from typing import Tuple, List, Dict

from .circle import Circle


class Segment:

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_segment_of(self, arr: np.ndarray) -> np.ndarray:
        return arr[self.y1:self.y2+1, self.x1:self.x2+1]

    def get_area(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    def draw_segment(self, image):
        cv.rectangle(image, (self.x1, self.y1), (self.x2, self.y2), (125, 100, 0), 0)


class SegmentedCircle:

    def __init__(self, circle: Circle):
        self.circle = circle
        self.segments: List[Segment] = []

    def add_segment(self, segment:Segment):
        self.segments.append(segment)

    def draw(self, image: np.ndarray):
        cv.circle(image, (self.circle.x, self.circle.y), self.circle.r, (0, 255, 0), 2)
        for segment in self.segments:
            segment.draw_segment(image)