from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.MethodExecutor import MethodExecutor
from modules.ActionExecutor import ActionExecutor
from modules.TimeControl import TimeControl


class SendHeroesToWork:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._time_to_check_heroes = TimeControl(60 * 20)
        self._image_processor = bomb_crypto_image_processor

    def run(self, image):
        if not self._time_to_check_heroes.is_expired():
            return False

        if self._image_processor.is_in_the_heroes_screen(image):
            return False

        if not self._image_processor.is_in_the_game_play_screen(image):
            return False

        is_go_heroes_button_visible = self.go_to_heroes_from_game_play(image)

        if is_go_heroes_button_visible:
            execution_result = MethodExecutor.execute(self.go_to_heroes_list,
                                                      [self._image_processor.image],
                                                      self._image_processor.is_in_the_heroes_screen,
                                                      [self._image_processor.image])

            if execution_result == MethodExecutor.SUCCESS:
                self._time_to_check_heroes.start()

        return True

    def go_to_heroes_list(self, image):
        go_to_heroes = self._image_processor.go_to_heroes(image)

        if go_to_heroes:
            ActionExecutor.click(go_to_heroes.single_random_point())
            return True

        return False

    def go_to_heroes_from_game_play(self, image):
        if not self._image_processor.is_in_the_game_play_screen(image):
            return False

        return MethodExecutor.execute(self.slide_to_get_access_go_heroes_button,
                                      [image],
                                      self._image_processor.go_to_heroes,
                                      [self._image_processor.image])

    def slide_to_get_access_go_heroes_button(self, image):
        slide_up_to_go_heroes = self._image_processor.slide_up_to_go_heroes(image)

        if slide_up_to_go_heroes:
            ActionExecutor.click(slide_up_to_go_heroes.single_random_point())
            return True

        return False
