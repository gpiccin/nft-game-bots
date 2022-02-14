from source.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from source.bombcrypto.BombCryptoImageProvider import BombCryptoImageProvider
from source.modules.ActionExecutor import ActionExecutor
from source.modules.MethodExecutionResult import MethodExecutionResult
from source.modules.MethodExecutor import MethodExecutor


class BombCryptoActionExecutor:
    def __init__(self, bomb_crypto_image_provider: BombCryptoImageProvider,
                 bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._bomb_crypto_image_provider = bomb_crypto_image_provider
        self._bomb_crypto_image_processor = bomb_crypto_image_processor

    def click(self, point):
        x, y = point

        if self._bomb_crypto_image_provider.top_left_corner is None:
            return

        screen_point = self._bomb_crypto_image_provider.top_left_corner.first_rectangle().left + x, \
                       self._bomb_crypto_image_provider.top_left_corner.first_rectangle().top + y

        ActionExecutor.click(screen_point)

    @staticmethod
    def drag(x_offset=0, y_offset=0, duration=0.0):
        ActionExecutor.drag(x_offset, y_offset, duration)

    def close_pop_up_on_game_play_screen(self) -> MethodExecutionResult:
        return MethodExecutor.execute(self._click_close_pop_up,
                                      [self._bomb_crypto_image_provider.game_screenshot],
                                      self._bomb_crypto_image_processor.is_in_the_game_play_screen,
                                      [self._bomb_crypto_image_provider.game_screenshot],
                                      seconds_waiting=2)

    def return_heroes_to_work(self) -> MethodExecutionResult:
        result = MethodExecutor.execute(self._click_coin_image,
                                        [self._bomb_crypto_image_provider.game_screenshot],
                                        self._bomb_crypto_image_processor.is_playing,
                                        [self._bomb_crypto_image_provider.game_screenshot])

        if result.is_failed():
            result = self.go_back()

        return result

    def go_to_treasure_hunt(self) -> MethodExecutionResult:
        return MethodExecutor.execute(self._click_go_to_treasure_hunt,
                                      [self._bomb_crypto_image_provider.game_screenshot],
                                      self._bomb_crypto_image_processor.is_in_the_game_play_screen,
                                      [self._bomb_crypto_image_provider.game_screenshot])

    def go_back(self) -> MethodExecutionResult:
        return MethodExecutor.execute(self._click_go_back,
                                      [self._bomb_crypto_image_provider.game_screenshot],
                                      self._bomb_crypto_image_processor.is_treasure_hunt_screen,
                                      [self._bomb_crypto_image_provider.game_screenshot])

    def send_all_heroes_to_work(self) -> MethodExecutionResult:
        return MethodExecutor.execute(self._click_all_heroes_to_work,
                                      [self._bomb_crypto_image_provider.game_screenshot],
                                      self._bomb_crypto_image_processor.is_all_working,
                                      [self._bomb_crypto_image_provider.game_screenshot], seconds_waiting=5)

    def go_to_heroes(self):
        return MethodExecutor.execute(self._click_hero_icon,
                                      [self._bomb_crypto_image_provider.game_screenshot],
                                      self._bomb_crypto_image_processor.is_in_the_heroes_screen,
                                      [self._bomb_crypto_image_provider.game_screenshot])

    def reveal_hero_icon_on_game_play_screen(self):
        return MethodExecutor.execute(self._click_slide_to_get_access_go_hero_icon,
                                      [self._bomb_crypto_image_provider.game_screenshot],
                                      self._bomb_crypto_image_processor.has_hero_icon,
                                      [self._bomb_crypto_image_provider.game_screenshot])

    def _click_go_to_treasure_hunt(self, image):
        treasure_hunt = self._bomb_crypto_image_processor.treasure_hunt(image)

        if treasure_hunt:
            self.click(treasure_hunt.single_random_point())

    def _click_slide_to_get_access_go_hero_icon(self, image):
        slide_up_to_go_heroes = self._bomb_crypto_image_processor.slide_up_to_go_heroes(image)

        if slide_up_to_go_heroes:
            self.click(slide_up_to_go_heroes.single_random_point())

    def _click_hero_icon(self, image):
        go_to_heroes = self._bomb_crypto_image_processor.go_to_heroes(image)

        if go_to_heroes:
            self.click(go_to_heroes.single_random_point())

    def _click_all_heroes_to_work(self, image):
        all_to_work = self._bomb_crypto_image_processor.all_heroes_to_work(image)

        if all_to_work:
            self.click(all_to_work.single_random_point())

    def _click_close_pop_up(self, image):
        close = self._bomb_crypto_image_processor.close(image)

        if close:
            self.click(close.single_random_point())

    def _click_coin_image(self, image):
        coin = self._bomb_crypto_image_processor.coin(image)

        if coin:
            self.click(coin.single_random_point())

    def _click_go_back(self, image):
        back = self._bomb_crypto_image_processor.back(image)

        if back:
            self.click(back.single_random_point())
