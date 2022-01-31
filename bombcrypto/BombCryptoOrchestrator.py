import logging
import sys
import time

from bombcrypto.BombCryptoBot import BombCryptoBot
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ImageLoader import ImageLoader
from modules.ImageProvider import ImageProvider


class BombCryptoOrchestrator:
    def __init__(self, image_provider: ImageProvider,
                 target_images_loader: ImageLoader):
        self._logger = logging.getLogger(type(self).__name__)
        self._image_provider = image_provider
        self.target_images_loader = target_images_loader
        self._bots = []
        self._seconds_to_check_bots = 3 * 60
        self._seconds_between_bot_execution = 2.5

    def read_bots(self):
        self._bots = []

        image = self._image_provider.screenshot()
        bomb_crypto_image_processor = BombCryptoImageProcessor(self._image_provider, self.target_images_loader)
        left_corners = bomb_crypto_image_processor.top_left_corner(image)

        if left_corners is None:
            return

        left_corners_rectangles = left_corners.rectangles()

        for left_corner in left_corners_rectangles:
            bot_bomb_crypto_image_processor =  BombCryptoImageProcessor(self._image_provider, self.target_images_loader)
            self._bots.append(BombCryptoBot(left_corner, bot_bomb_crypto_image_processor))

    def has_more_than_one_bot(self):
        return len(self._bots) > 1

    def run(self):
        self.read_bots()

        for bot in self._bots:
            self._logger.info('Run bot ' + bot.id)

            if self.has_more_than_one_bot():
                bot.maximize_window()

            while True:
                if not bot.run():
                    break
                else:
                    self._logger.info('Waiting ' + str(self._seconds_between_bot_execution) +
                                      ' seconds to execute a new bot ' + bot.id + ' command')

                    time.sleep(self._seconds_between_bot_execution)

            if self.has_more_than_one_bot():
                bot.return_window_size()

        self._logger.info('Waiting ' + str(self._seconds_to_check_bots) + ' seconds to check bots again')
        time.sleep(self._seconds_to_check_bots)
