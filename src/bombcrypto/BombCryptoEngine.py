from src.modules.ImageProcessor import ImageProcessor
from src.modules.ImageLoader import ImageLoader
from src.modules.ImageProvider import ImageProvider
from src.bombcrypto.BombCryptoActions import ClickConnectWallet, ClickOkError, ClickOk, ClickSignOnMetamask
from src.modules.Actions import Action


class BombCryptoEngine:
    def __init__(self, image_provider: ImageProvider, match_image_threshold=0.7, debug=True):
        self._debug = debug
        self._target_images = None
        self._match_image_threshold = match_image_threshold
        self._image_processor = ImageProcessor()
        self._image_provider = image_provider

    def actions(self) -> []:
        self._target_images = ImageLoader('./bombcrypto/target-images')
        self._target_images.load()

        image = self._image_provider.image()

        actions = []

        self._append_action(self.connect_wallet(image), actions)
        self._append_action(self.error(image), actions)
        self._append_action(self.generic_ok(image), actions)
        self._append_action(self.sign_metamask(image), actions)

        self._debug_image(image, actions)

        return actions

    def connect_wallet(self, image) -> ClickConnectWallet:
        images = ['connect-wallet-button-0', 'connect-wallet-button-1', 'connect-wallet-button-2',
                  'connect-wallet-button-3']
        rectangle, is_connect_wallet_screen = self._image_processor.match_list(image, self._target_images, images,
                                                                               self._match_image_threshold)

        if is_connect_wallet_screen:
            return ClickConnectWallet(rectangle)

        return None

    def error(self, image) -> ClickOkError:
        images = ['error-0', 'error-1001-0', 'error-server-unstable-0']
        rectangle, is_error_screen = self._image_processor.match_list(image, self._target_images, images,
                                                                      self._match_image_threshold)

        if is_error_screen:
            generic_ok = self.generic_ok(image)

            if generic_ok:
                return ClickOkError(generic_ok.rectangle())

        return None

    def generic_ok(self, image) -> ClickOk:
        images = ['ok-0', 'ok-1', 'ok-2']
        rectangle, has_ok_button_on_the_screen = self._image_processor.match_list(image, self._target_images, images,
                                                                      self._match_image_threshold)

        if has_ok_button_on_the_screen:
            return ClickOk(rectangle)

        return None

    def sign_metamask(self, image) -> ClickSignOnMetamask:
        images = ['sign-metamask-0', 'sign-metamask-1']
        rectangle, has_sign_button_on_the_screen = self._image_processor.match_list(image, self._target_images, images,
                                                                      self._match_image_threshold)

        if has_sign_button_on_the_screen:
            return ClickSignOnMetamask(rectangle)

        return None

    def _debug_image(self, image, actions):
        if not self._debug:
            return

        for action in actions:
            if type(action) is ClickConnectWallet:
                for _ in range(100):
                    ImageProcessor.draw_circle(image, action.point())

        ImageProcessor.show(image)

    @staticmethod
    def _append_action(action, actions):
        if action:
            actions.append(action)
