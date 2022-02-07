from typing import Optional

from source.modules.Behaviours import Information
from source.modules.ImageProcessor import ImageProcessor
from source.modules.ImageProvider import ImageProvider


class BombCryptoImageProvider:
    def __init__(self, image_provider: ImageProvider):
        self._image_provider = image_provider
        self.bottom_right_corner: Optional[Information] = None
        self.top_left_corner: Optional[Information] = None

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

    def game_screenshot(self):
        print_screen_image = self._image_provider.screenshot()
        game_screen = self.cut_image(print_screen_image)
        return game_screen

    def screenshot(self):
        print_screen_image = self._image_provider.screenshot()
        return print_screen_image

    def images(self):
        return self._image_provider.images()
