import logging
import time
from typing import List, Optional

from source.bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from source.bombcrypto.BombCryptoBot import BombCryptoBot
from source.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from source.bombcrypto.BombCryptoImageProvider import BombCryptoImageProvider
from source.modules.Configurations import Configurations
from source.modules.ImageLoader import ImageLoader
from source.modules.ImageProcessor import ImageProcessor
from source.modules.ImageProvider import ImageProvider
from source.modules.Rectangle import Rectangle
from source.modules.TimeControl import TimeControl


class BombCryptoOrchestrator:
    def __init__(self, image_provider: ImageProvider,
                 target_images_loader: ImageLoader,
                 configurations: Configurations):
        self._logger = logging.getLogger(type(self).__name__)
        self._image_provider = image_provider
        self.target_images_loader = target_images_loader
        self._bots = {}
        self._seconds_to_check_bots = 4 * 60
        self._seconds_between_bot_execution = 1
        self._max_seconds_waiting_bot_actions = 10 * 60
        self._configurations = configurations

    def _remove_bots_not_found(self, read_keys):
        keys_to_remove = []

        for key in self._bots.keys():
            if key not in read_keys:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            self._bots.pop(key)

    @staticmethod
    def read_keys(left_corners_rectangles: List[Rectangle]) -> List[str]:
        keys = []

        for left_corner in left_corners_rectangles:
            keys.append(BombCryptoBot.create_id(left_corner))

        return keys

    def read_left_corners(self) -> Optional[List[Rectangle]]:
        bomb_crypto_image_processor = self.create_bomb_crypto_image_processor()

        image = self._image_provider.screenshot()
        left_corners = bomb_crypto_image_processor.top_left_corner(image)

        # copied = image.copy()
        # ImageProcessor.draw_rectangles(copied, left_corners.rectangles())
        # ImageProcessor.show(copied)

        if left_corners is None:
            return None

        return left_corners.rectangles()

    def create_bomb_crypto_image_processor(self):
        bomb_crypto_image_provider = BombCryptoImageProvider(self._image_provider)
        return BombCryptoImageProcessor(bomb_crypto_image_provider,
                                        self.target_images_loader,
                                        match_image_threshold=self._configurations.image_analysis_accuracy())

    def create_bot(self, left_corner):
        image_provider = BombCryptoImageProvider(self._image_provider)
        image_processor = BombCryptoImageProcessor(image_provider,
                                                   self.target_images_loader,
                                                   match_image_threshold=self._configurations.image_analysis_accuracy())
        action_executor = BombCryptoActionExecutor(image_provider, image_processor)

        return BombCryptoBot(left_corner, image_provider,
                             image_processor,
                             action_executor)

    def read_bots(self):
        left_corners = self.read_left_corners()

        if left_corners is None:
            return

        keys = BombCryptoOrchestrator.read_keys(left_corners)
        self._remove_bots_not_found(keys)

        for left_corner in left_corners:
            bot_id = BombCryptoBot.create_id(left_corner)

            if bot_id not in self._bots.keys():
                self._bots[bot_id] = self.create_bot(left_corner)

    def has_more_than_one_bot(self):
        return len(self._bots) > 1

    def start(self):
        while True:
            #try:
            self._run()
            #except Exception as e:
            #    self._logger.error(str(e))

    def _run(self):
        self.read_bots()

        self._logger.info(str(len(self._bots)) + ' bots identified')

        for bot_key in self._bots:
            bot: BombCryptoBot = self._bots[bot_key]
            self._logger.info('Run bot ' + bot.id)

            if self.has_more_than_one_bot():
                bot.maximize_window()

            time_running_bot = TimeControl(self._max_seconds_waiting_bot_actions)
            time_running_bot.start()

            while not time_running_bot.is_expired():
                if bot.run().executed():
                    self._logger.info('Waiting ' + str(self._seconds_between_bot_execution) +
                                      ' seconds to execute a new bot ' + bot.id + ' command')
                    time.sleep(self._seconds_between_bot_execution)
                else:
                    break

            if self.has_more_than_one_bot():
                bot.return_window_size()

        self._logger.info('Waiting ' + str(self._seconds_to_check_bots) + ' seconds to check bots again')
        time.sleep(self._seconds_to_check_bots)
