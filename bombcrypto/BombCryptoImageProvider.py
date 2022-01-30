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
        pass
