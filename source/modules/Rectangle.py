from random import uniform

from pyrect import Rect


class Rectangle(Rect):
    def __init__(self, ndarray, enable_float=False, read_only=False, on_change=None, on_read=None):
        x_bar, y_bar, w_bar, h_bar = ndarray

        if enable_float:
            super().__init__(float(x_bar), float(y_bar), float(w_bar), float(h_bar), enable_float, read_only, on_change,
                             on_read)
        else:
            super().__init__(int(x_bar), int(y_bar), int(w_bar), int(h_bar), enable_float, read_only, on_change,
                             on_read)

    def random_point(self):
        position_x = self.left + self.width * uniform(0.1, 0.9)
        position_y = self.top + self.height * uniform(0.1, 0.9)
        return position_x, position_y

    def to_string(self):
        return str(self.top) + ':' + str(self.left)

    def rectangle(self):
        return self.x, self.y, self.width, self.height

    @staticmethod
    def create_list(rectangles, enable_float=False, read_only=False, on_change=None, on_read=None) -> []:
        new_rectangles = []

        for rect in rectangles:
            new_rectangles.append(Rectangle(rect, enable_float, read_only, on_change, on_read))

        return new_rectangles
