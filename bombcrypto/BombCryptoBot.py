import sys
import time

from bombcrypto.AllStrategy import AllStrategy
from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.BombCryptoImageProvider import BombCryptoImageProvider
from bombcrypto.ConnectWallet import ConnectWallet
from bombcrypto.GenericClose import GenericClose
from bombcrypto.GenericOk import GenericOk
from bombcrypto.GreenBarStrategy import GreenBarStrategy
from bombcrypto.HeroReader import HeroReader
from bombcrypto.SendHeroesToWork import SendHeroesToWork
from bombcrypto.Sign import Sign
from bombcrypto.TreasureHunt import TreasureHunt
from bombcrypto.UnlockHeroes import UnlockHeroes
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutionResult import MethodExecutionResultFactory, MethodExecutionResult
from modules.Rectangle import Rectangle


class BombCryptoBot:
    def __init__(self, position: Rectangle,
                 bomb_crypto_image_provider: BombCryptoImageProvider,
                 bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self.id = BombCryptoBot.create_id(position)
        self.top_left_position = position
        self._wait_seconds_after_resize_window = 2.5
        self._bomb_crypto_image_provider = bomb_crypto_image_provider
        self._bomb_crypto_image_processor = bomb_crypto_image_processor
        self._action_executor = action_executor
        self._sign = Sign(self._bomb_crypto_image_processor, self._action_executor)
        self._connect_wallet = ConnectWallet(self._bomb_crypto_image_processor, self._action_executor)
        self._treasure_hunt = TreasureHunt(self._bomb_crypto_image_processor, self._action_executor)
        self._go_to_heroes = SendHeroesToWork(self._bomb_crypto_image_processor, self._action_executor)
        self._heroes_reader = HeroReader(self._bomb_crypto_image_processor, self._action_executor)
        self._green_bar_strategy = GreenBarStrategy(self._bomb_crypto_image_processor, self._heroes_reader,
                                                    self._action_executor)
        self._all_strategy = AllStrategy(self._bomb_crypto_image_processor, self._action_executor)
        self._unlock_heroes = UnlockHeroes(self._bomb_crypto_image_processor, self._action_executor)
        self._generic_close = GenericClose(self._bomb_crypto_image_processor, self._action_executor)
        self._generic_ok = GenericOk(self._bomb_crypto_image_processor)

    @staticmethod
    def create_id(position: Rectangle):
        return 'bot:' + position.to_string()

    def maximize_window(self):
        ActionExecutor.click(self.top_left_position.random_point())
        ActionExecutor.maximize()
        time.sleep(self._wait_seconds_after_resize_window)

    def return_window_size(self):
        image = self._bomb_crypto_image_processor.game_screenshot()
        left_corner = self._bomb_crypto_image_processor.top_left_corner(image)

        if left_corner is None:
            return

        self._action_executor.click(left_corner.first_rectangle().random_point())
        ActionExecutor.maximize()
        time.sleep(self._wait_seconds_after_resize_window)

    def update_screen_position(self, image):
        top_left = self._bomb_crypto_image_processor.top_left_corner(image)

        if top_left is None:
            self._bomb_crypto_image_provider.set_unknown_game_position()
            return

        bottom_right = self._bomb_crypto_image_processor.bottom_right_corner(image)

        if bottom_right is None:
            self._bomb_crypto_image_provider.set_unknown_game_position()
            return

        self._bomb_crypto_image_provider.set_top_left_corner(top_left)
        self._bomb_crypto_image_provider.set_bottom_right_corner(bottom_right)

    def run(self) -> MethodExecutionResult:
        screenshot = self._bomb_crypto_image_processor.screenshot()

        if screenshot is None:
            return MethodExecutionResultFactory.not_executed()

        self.update_screen_position(screenshot)

        if not self._bomb_crypto_image_provider.is_actionable():
            return MethodExecutionResultFactory.not_executed()

        game_screenshot = self._bomb_crypto_image_processor.game_screenshot()

        result = self._generic_ok.run(game_screenshot)
        if result.executed():
            return result

        result = self._sign.run(game_screenshot)
        if result.executed():
            return result

        result = self._connect_wallet.run(game_screenshot)
        if result.executed():
            return result

        result = self._treasure_hunt.run(game_screenshot)
        if result.executed():
            return result

        result = self._go_to_heroes.run(game_screenshot)
        if result.executed():
            return result

        result = self._green_bar_strategy.run(game_screenshot)
        if result.executed():
            return result

        result = self._unlock_heroes.run(game_screenshot)
        if result.executed():
            return result

        result = self._generic_close.run(game_screenshot)
        if result.executed():
            return result

        sys.stdout.write('.')
        sys.stdout.flush()

        return MethodExecutionResultFactory.unknown()
