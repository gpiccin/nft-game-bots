from random import uniform

class Action:
    def __init__(self):
        self._click_position = 1
        self._target_rectangle = 1


class Unknow(Action):
    def __init__(self):
        super().__init__()


class Refresh(Action):
    def __init__(self):
        super().__init__()


class Click(Action):
    def __init__(self, rectangle):
        super().__init__()
        self._rectangle = rectangle

    def rectangle(self):
        return self._rectangle

    def point(self):
        x, y, width, height = self._rectangle[0]

        position_x = x + width * uniform(0.1, 0.9)
        position_y = y + height * uniform(0.1, 0.9)

        return int(position_x), int(position_y)
