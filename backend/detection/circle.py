from typing import Tuple, List, Dict


class Circle:
    def __init__(self, circle: Tuple):
        circle = [int(c) for tuple in circle for c in tuple]
        self.x = circle[0]
        self.y = circle[1]
        self.r = circle[2]

    def get_as_tuple(self):
        return self.x, self.y, self.r
