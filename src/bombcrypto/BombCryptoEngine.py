from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageLoader import ImageLoader
from src.modules.ImageProvider import ImageProvider
from src.bombcrypto.BombCryptoActions import ConnectWallet
from src.modules.Actions import Action


class BombCryptoEngine:
    def __init__(self, image_provider: ImageProvider, match_image_threshold=0.8, debug=True):
        self._target_images = None
        self._match_image_threshold = match_image_threshold
        self._image_processor = ImageProcessor(debug)
        self._image_provider = image_provider

    def actions(self) -> []:
        self._target_images = ImageLoader('./bombcrypto/target-images')
        self._target_images.load()

        image = self._image_provider.image()

        actions = []

        self._append_action(self._connect_wallet(image), actions)

        for action in actions:
            if type(action) is ConnectWallet:
                for _ in range(1000):
                    ImageProcessor.draw_circle(image, action.point())

        ImageProcessor.show(image)

        return actions

    @staticmethod
    def _append_action(action, actions):
        if action:
            actions.append(action)

    def _connect_wallet(self, image) -> Action:
        images = ['connect-wallet', 'connect-wallet-button-1', 'connect-wallet-button-2', 'connect-wallet-button-3']
        rectangle, is_connect_wallet_screen = self._image_processor.match_list(image, self._target_images, images, self._match_image_threshold)

        if is_connect_wallet_screen:
            return ConnectWallet(rectangle)

        return None
