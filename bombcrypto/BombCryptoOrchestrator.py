import logging
import sys
import time

from bombcrypto.BombCryptoBot import BombCryptoBot
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor


class BombCryptoOrchestrator:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._logger = logging.getLogger(type(self).__name__)
        self._bomb_crypto_image_processor = bomb_crypto_image_processor
        self._bots = []
        self._seconds_to_check_bots = 3 * 60

    def read_bots(self):
        self._bots = []

        image = self._bomb_crypto_image_processor.screenshot()
        left_corners = self._bomb_crypto_image_processor.top_left_corner(image)

        if left_corners is None:
            return

        left_corners_rectangles = left_corners.rectangles()

        for left_corner in left_corners_rectangles:
            self._bots.append(BombCryptoBot(left_corner, self._bomb_crypto_image_processor))

    def has_more_than_one_bot(self):
        return len(self._bots) > 1

    def run(self):
        self.read_bots()

        for bot in self._bots:
            if self.has_more_than_one_bot():
                bot.maximize_window()

            while True:
                if not bot.run():
                    break

            if self.has_more_than_one_bot():
                bot.return_window_to_default()

        self._logger.info('Waiting ' + str(self._seconds_to_check_bots) + ' seconds to check bots again')
        time.sleep(self._seconds_to_check_bots)
