from random import uniform


class Behaviour:
    def __init__(self):
        self._click_position = 1
        self._target_rectangle = 1


class Unknow(Behaviour):
    def __init__(self):
        super().__init__()


class Refresh(Behaviour):
    def __init__(self):
        super().__init__()


class Click(Behaviour):
    def __init__(self, rectangles):
        super().__init__()
        self._rectangles = rectangles

    def rectangle(self):
        return self._rectangles

    def points(self) -> []:
        points = []

        for rectangle in self._rectangles:
            x, y, width, height = rectangle

            position_x = x + width * uniform(0.1, 0.9)
            position_y = y + height * uniform(0.1, 0.9)

            points.append((int(position_x), int(position_y)))

        return points
