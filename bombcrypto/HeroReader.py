import logging
import time
from typing import Optional

from bombcrypto.BombCryptoActionExecutor import BombCryptoActionExecutor
from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.Hero import Hero
from bombcrypto.HeroList import HeroList
from modules.Rectangle import Rectangle


class HeroReader:
    def __init__(self, image_processor: BombCryptoImageProcessor,
                 action_executor: BombCryptoActionExecutor):
        self._logger = logging.getLogger(type(self).__name__)
        self._action_executor = action_executor
        self._last_hero_point = None
        self._first_hero_point = None
        self._hero_height = None
        self._image_processor = image_processor
        self._first_scroll_y_offset = -324
        self._second_scroll_y_offset = -300
        self._seconds_to_wait_before_read_screen = 1.6

    def scroll_up_heroes_list(self):
        self._action_executor.click(self._first_hero_point)
        self._action_executor.drag(0, 420, 0.2)

    def scroll_last_heroes_page(self):
        self._action_executor.click(self._last_hero_point)
        self._action_executor.drag(0, -420, 0.2)

    def scroll_up_middle_heroes_list(self, y_offset, duration=2.2):
        self._action_executor.click(self._first_hero_point)
        self._action_executor.drag(0, y_offset, duration)
        self._action_executor.click(self._first_hero_point)

    def scroll_down_heroes_list(self, y_offset, duration=2.2):
        self._action_executor.click(self._last_hero_point)
        self._action_executor.drag(0, y_offset, duration)
        self._action_executor.click(self._first_hero_point)

    def load_all_heroes(self) -> HeroList:
        heroes = HeroList()
        heroes.add_list(self.read_heroes_from_screen(wait_to_read=False))

        if len(heroes) == 5:
            self.scroll_down_heroes_list(self._first_scroll_y_offset)
            heroes.add_list(self.read_heroes_from_screen())

        if len(heroes) == 10:
            self.scroll_down_heroes_list(self._second_scroll_y_offset, 0.2)
            heroes.add_list(self.read_heroes_from_screen())

        self._logger.info(str(len(heroes)) + ' heroes loaded')

        for hero in heroes:
            self._logger.info('ID:' + hero.id + ' | EL:' + str(hero.energy_level))

        return heroes

    def find_hero(self, id_image) -> Optional[Hero]:
        hero = self._get_hero_from_screen(id_image)
        if hero:
            return hero

        self.scroll_up_heroes_list()
        hero = self._get_hero_from_screen(id_image)
        if hero:
            return hero

        self.scroll_down_heroes_list(self._first_scroll_y_offset)
        hero = self._get_hero_from_screen(id_image)
        if hero:
            return hero

        self.scroll_down_heroes_list(self._second_scroll_y_offset, 0.2)
        hero = self._get_hero_from_screen(id_image)
        if hero:
            return hero

        return None

    def _get_hero_from_screen(self, id_image) -> Optional[Hero]:
        heroes = self.read_heroes_from_screen()

        if heroes is None:
            return None

        return heroes.get_hero(id_image, 0.995)

    def read_heroes_from_screen(self, wait_to_read=True) -> Optional[HeroList]:
        self._logger.info('Read heroes')

        if wait_to_read:
            self._logger.info('Waiting ' + str(self._seconds_to_wait_before_read_screen) + ' seconds to read')
            time.sleep(self._seconds_to_wait_before_read_screen)

        image = self._image_processor.game_screenshot()
        self.update_heroes_position_information(image)

        bars = self._image_processor.hero_bar(image)
        work_buttons = self._image_processor.work(image)
        rest_buttons = self._image_processor.rest(image)

        if bars is None or work_buttons is None or rest_buttons is None:
            return None

        bar_rectangles = bars.rectangles()
        work_button_rectangle_reference = work_buttons.first_rectangle()
        rest_button_rectangle_reference = rest_buttons.first_rectangle()

        heroes = HeroList()

        for bar_rectangle in bar_rectangles:
            estimated_work_rectangle = HeroReader._create_estimated_button_position(bar_rectangle,
                                                                                    work_button_rectangle_reference)

            estimated_rest_rectangle = HeroReader._create_estimated_button_position(bar_rectangle,
                                                                                    rest_button_rectangle_reference)

            hero = Hero(image,
                        bar_rectangle,
                        estimated_work_rectangle,
                        estimated_rest_rectangle,
                        self._image_processor)

            heroes.add(hero)

            self._logger.info('ID:' + hero.id + ' | EL:' + str(hero.energy_level))

        self._logger.info(str(len(heroes)) + ' heroes read')

        return heroes

    @staticmethod
    def _create_estimated_button_position(bar_rectangle: Rectangle,
                                          reference_button: Rectangle) -> Rectangle:
        return Rectangle(
            (
                reference_button.right - reference_button.width,
                bar_rectangle.top + 8,
                reference_button.width,
                reference_button.height
            )
        )

    def update_heroes_position_information(self, image):
        bars = self._image_processor.hero_bar(image)

        first_bar = bars.first_rectangle()

        self._first_hero_point = (first_bar.left - 5, first_bar.top)
        self._hero_height = first_bar.height

        last_bar = bars.last_rectangle()
        self._last_hero_point = last_bar.bottomleft
