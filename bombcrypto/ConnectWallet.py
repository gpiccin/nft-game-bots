from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutionResult import MethodExecutionResultFactory, MethodExecutionResult
from modules.MethodExecutor import MethodExecutor


class ConnectWallet:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image) -> MethodExecutionResult:
        if not self._image_processor.is_connect_wallet_screen(image):
            return MethodExecutionResultFactory.not_executed()

        result = MethodExecutor.execute(self._click_connect,
                                        [image],
                                        self._image_processor.is_sign_screen,
                                        [self._image_processor.screenshot],
                                        seconds_waiting=10)

        if result.is_success():
            return MethodExecutionResultFactory.success()

        ActionExecutor.refresh_page()
        return MethodExecutionResultFactory.fail()

    def _click_connect(self, image):
        connect_wallet = self._image_processor.connect_wallet(image)

        if connect_wallet:
            self._action_executor.click(connect_wallet.single_random_point())
