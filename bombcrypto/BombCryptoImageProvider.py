from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ImageProcessor import ImageProcessor
from modules.ImageProvider import ImageProvider


class BombCryptoImageProvider:
    def __init__(self, image_provider: ImageProvider,
                 image_processor: BombCryptoImageProcessor):
        self._image_processor = image_processor
        self._image_provider = image_provider

    def set_current(self):
        pass

    def image(self):
        print_screen_image = self._image_provider.image()

        top_left = self._image_processor.top_left_corner(print_screen_image)

        if top_left is None:
            return None

        top_right = self._image_processor.top_right_corner(print_screen_image)
        bottom_left = self._image_processor.bottom_left_corner(print_screen_image)

        trx, tr_y, trw, trh = top_right.first_rectangle()
        tlx, tly, tlw, tlh = top_left.first_rectangle()
        blx, bly, blw, blh = bottom_left.first_rectangle()

        image = print_screen_image[tly:bly + blh, tlx:tlx + trx + tlw]

        ImageProcessor.show(image)

        return image
