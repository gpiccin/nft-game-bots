from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageLoader import ImageLoader


class BombCryptoBot:
    def __init__(self, match_image_threshold=0.8, debug=True):
        self._test_images = None
        self._target_images = None
        self._match_image_threshold = match_image_threshold
        self._image_processor = ImageProcessor(debug)

    def run(self):
        self._target_images = ImageLoader('./bombcrypto/target-images')
        self._test_images = ImageLoader('./bombcrypto/test-images')
        self._target_images.load()
        self._test_images.load()

        self.connect_wallet(self._test_images.get_image('connect_wallet'))

    def connect_wallet(self, image):
        images = ['connect-wallet', 'connect-wallet-button-1', 'connect-wallet-button-2', 'connect-wallet-button-3']
        return self._image_processor.match_list(image, self._target_images, images, self._match_image_threshold)