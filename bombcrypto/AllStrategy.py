from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ActionExecutor import ActionExecutor
from modules.MethodExecutor import MethodExecutor


class AllStrategy:
    def __init__(self,
                 bomb_crypto_image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._action_executor = action_executor
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        if not self._image_processor.is_in_the_heroes_screen(image):
            return False

        execution_result = MethodExecutor.execute(self.all,
                                                  [self._image_processor.game_screenshot],
                                                  self._image_processor.is_all_working,
                                                  [self._image_processor.game_screenshot], seconds_waiting=5)

        if execution_result == MethodExecutor.SUCCESS:
            execution_result = MethodExecutor.execute(self.close,
                                                      [self._image_processor.game_screenshot],
                                                      self._image_processor.is_in_the_game_play_screen,
                                                      [self._image_processor.game_screenshot], seconds_waiting=2)

        if execution_result == MethodExecutor.SUCCESS:
            execution_result = MethodExecutor.execute(self.return_to_work,
                                                      [self._image_processor.game_screenshot],
                                                      self._image_processor.is_playing,
                                                      [self._image_processor.game_screenshot], seconds_waiting=2)

            if execution_result == MethodExecutor.FAIL:
                MethodExecutor.execute(self.go_to_back,
                                       [image],
                                       self._image_processor.is_treasure_hunt_screen,
                                       [self._image_processor.game_screenshot])

        return True

    def all(self, image):
        all_to_work = self._image_processor.all_heroes_to_work(image)

        if all_to_work:
            self._action_executor.click(all_to_work.single_random_point())

    def close(self, image):
        close = self._image_processor.close(image)

        if close:
            self._action_executor.click(close.single_random_point())

    def return_to_work(self, image):
        coin = self._image_processor.coin(image)

        if coin:
            self._action_executor.click(coin.single_random_point())

    def go_to_back(self, image):
        back = self._image_processor.back(image)

        if back:
            self._action_executor.click(back.single_random_point())
