from typing import List, Optional

from modules.Rectangle import Rectangle


class Behaviour:
    def __init__(self):
        self._click_position = 1
        self._target_rectangle = 1


class Information(Behaviour):
    def __init__(self, rectangles):
        super().__init__()
        self._rectangles = rectangles

    def first_rectangle(self) -> Optional[Rectangle]:
        if len(self._rectangles) == 0:
            return None

        return self._rectangles[0]

    def last_rectangle(self) -> Optional[Rectangle]:
        if len(self._rectangles) == 0:
            return None

        return self._rectangles[len(self._rectangles) - 1]

    def rectangles(self) -> List[Rectangle]:
        return self._rectangles


class Unknown(Behaviour):
    def __init__(self):
        super().__init__()


class Refresh(Behaviour):
    def __init__(self):
        super().__init__()


class Click(Information):
    def __init__(self, rectangles):
        super().__init__(rectangles)

    def single_random_point(self):
        points = self.random_points()

        if len(points) == 0:
            return None

        return points[0]

    def random_points(self):
        points = []

        for rectangle in self._rectangles:
            points.append(rectangle.random_point())

        return points
