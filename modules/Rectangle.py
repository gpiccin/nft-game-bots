from random import uniform

from pyrect import Rect


class Rectangle(Rect):
    def __init__(self, ndarray, enableFloat=False, readOnly=False, onChange=None, onRead=None):
        x_bar, y_bar, w_bar, h_bar = ndarray

        if enableFloat:
            super().__init__(float(x_bar), float(y_bar), float(w_bar), float(h_bar), enableFloat, readOnly, onChange, onRead)
        else:
            super().__init__(int(x_bar), int(y_bar), int(w_bar), int(h_bar), enableFloat, readOnly, onChange, onRead)

    def random_point(self):
        position_x = self.left + self.width * uniform(0.1, 0.9)
        position_y = self.top + self.height * uniform(0.1, 0.9)
        return position_x, position_y

    @staticmethod
    def create_list(rectangles, enableFloat=False, readOnly=False, onChange=None, onRead=None) -> []:
        new_rectangles = []

        for rect in rectangles:
            new_rectangles.append(Rectangle(rect, enableFloat, readOnly, onChange, onRead))

        return new_rectangles