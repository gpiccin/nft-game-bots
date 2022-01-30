from modules.ActionExecutor import ActionExecutor
from modules.ImageProcessor import ImageProcessor


class BombCryptoActionExecutor:
    def __init__(self):
        self.bottom_right_corner = None
        self.top_left_corner = None

    def set_top_left_corner(self, top_left_corner):
        self.top_left_corner = top_left_corner
        
    def set_bottom_right_corner(self, bottom_right_corner):
        self.bottom_right_corner = bottom_right_corner

    def set_unknown_game_position(self):
        self.bottom_right_corner = self.top_left_corner = None

    def is_actionable(self):
        return self.top_left_corner is not None and self.bottom_right_corner is not None

    def cut_image(self, image):
        return ImageProcessor.cut_rectangles(image, self.top_left_corner.first_rectangle(),
                                             self.bottom_right_corner.first_rectangle())

    def click(self, point):
        x, y = point
        screen_point = self.top_left_corner.first_rectangle().x + x, \
                       self.top_left_corner.first_rectangle().y + y
        ActionExecutor.click(screen_point)

    def drag(self, xOffset=0, yOffset=0, duration=0.0):
        ActionExecutor.drag(xOffset, yOffset, duration)