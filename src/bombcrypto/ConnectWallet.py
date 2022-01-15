import time

from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.modules.MouseExecutor import MouseExecutor


class TimeControl:
    def __init__(self):
        self._seconds_to_expire = None
        self._init = time.time()
        self._last_execution = 0

    def is_running(self):
        return self._last_execution != 0

    def refresh(self):
        self._last_execution = time.time()

    def wait_for_expire(self, seconds):
        self._seconds_to_expire = seconds

    def reset(self):
        self._last_execution = 0

    def elapsed_time(self):
        return time.time() - self._last_execution

    def is_expired(self):
        return not self.is_running() or self.elapsed_time() > self._seconds_to_expire


class ConnectWallet:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor, limit_seconds_to_wait_sign: int = 20):
        self._limit_seconds_to_wait_sign = limit_seconds_to_wait_sign
        self._limit_seconds_to_wait_after_sign = 5
        self._bomb_crypto_image_processor = bomb_crypto_image_processor
        self._time_after_sign = TimeControl()
        self._time_after_connect = TimeControl()

    def run(self):
        image = self._bomb_crypto_image_processor.image_provider().image()

        connect_wallet = self._bomb_crypto_image_processor.connect_wallet(image)

        if not connect_wallet:
            return

        sign_on_metamask_click = self._bomb_crypto_image_processor.sign_metamask(image)

        if sign_on_metamask_click and self._time_after_sign.is_expired():
            MouseExecutor.click(sign_on_metamask_click.points()[0])
            self._time_after_sign.wait_for_expire(self._limit_seconds_to_wait_after_sign)
            self._time_after_sign.refresh()
            self._time_after_connect.refresh()
            return

        if self._time_after_connect.is_expired():
            MouseExecutor.click(connect_wallet.points()[0])
            self._time_after_connect.wait_for_expire(self._limit_seconds_to_wait_sign)
            self._time_after_connect.refresh()
