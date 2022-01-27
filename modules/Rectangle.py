import imp
from pyrect import Rect

class Rectangle(Rect):
    def __init__(self, ndarray, enableFloat=False, readOnly=False, onChange=None, onRead=None):
        x_bar, y_bar, w_bar, h_bar = ndarray

        if enableFloat:
            super().__init__(float(x_bar), float(y_bar), float(w_bar), float(h_bar), enableFloat, readOnly, onChange, onRead)
        else:
            super().__init__(int(x_bar), int(y_bar), int(w_bar), int(h_bar), enableFloat, readOnly, onChange, onRead)
