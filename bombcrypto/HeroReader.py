import logging
import time
from typing import Optional

import pyautogui

from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from bombcrypto.Hero import Hero
from bombcrypto.HeroList import HeroList
from modules.ActionExecutor import ActionExecutor


class HeroReader:
    def __init__(self, image_processor: BombCryptoImageProcessor):
        self._logger = logging.getLogger(type(self).__name__)
        self._last_hero_point = None
        self._first_hero_point = None
        self._hero_height = None
        self._image_processor = image_processor
        self._first_scroll_adjust_factor = 6.55
        self._second_scroll_adjust_factor = 6.65
        self._seconds_to_wait_before_read_screen = 1.2

    def scroll_up_heroes_list(self, image=None):
        if image is None:
            image = self._image_processor.image()

        self.update_first_hero_point(image)
        ActionExecutor.click(self._first_hero_point)

        pyautogui.drag(0, self._hero_height * 15, duration=0.3, button='left')

    def scroll_down_heroes_list(self, adjust_factor):
        ActionExecutor.click(self._last_hero_point)

        pyautogui.drag(0, -self._hero_height * adjust_factor, duration=1, button='left')

        ActionExecutor.click(self._last_hero_point)

    def load_all_heroes(self, image) -> HeroList:
        self.update_first_hero_point(image)

        heroes = HeroList()
        heroes.add_list(self._read_heroes_from_screen())

        if len(heroes) == 5:
            self.scroll_down_heroes_list(self._first_scroll_adjust_factor)
            heroes.add_list(self._read_heroes_from_screen())

        if len(heroes) == 10:
            self.scroll_down_heroes_list(self._second_scroll_adjust_factor)
            heroes.add_list(self._read_heroes_from_screen())

        self._logger.info(str(len(heroes)) + ' heroes found')

        for hero in heroes:
            self._logger.info('ID:' + hero.id + ' | EL:' + str(hero.energy_level))

        return heroes

    def find_hero(self, id_image) -> Optional[Hero]:
        hero = self.get_hero(id_image)
        if hero:
            return hero

        self.scroll_up_heroes_list()
        hero = self.get_hero(id_image)
        if hero:
            return hero

        self.scroll_down_heroes_list(self._first_scroll_adjust_factor)
        hero = self.get_hero(id_image)
        if hero:
            return hero

        self.scroll_down_heroes_list(self._second_scroll_adjust_factor)
        hero = self.get_hero(id_image)
        if hero:
            return hero

        return None

    def get_hero(self, id_image) -> Optional[Hero]:
        heroes = self._read_heroes_from_screen()

        if heroes is None:
            return None

        return heroes.get_hero(id_image)

    def _read_heroes_from_screen(self) -> Optional[HeroList]:
        self._logger.info('Read heroes')

        time.sleep(self._seconds_to_wait_before_read_screen)
        image = self._image_processor.image()

        bars = self._image_processor.hero_bar(image)
        work_buttons = self._image_processor.work(image)
        rest_buttons = self._image_processor.rest(image)

        # self._image_processor.debug_image(image, [bars, rest_buttons])

        if bars is None or work_buttons is None or rest_buttons is None:
            return None

        bars_rectangles = bars.rectangles()
        work_buttons_rectangles = work_buttons.rectangles()
        rest_buttons_rectangles = rest_buttons.rectangles()

        if len(bars_rectangles) != len(work_buttons_rectangles) or \
                len(bars_rectangles) != len(rest_buttons_rectangles) or \
                len(work_buttons_rectangles) != len(rest_buttons_rectangles):
            return None

        self.update_last_hero_point(bars_rectangles[len(bars_rectangles) - 1])

        heroes = HeroList()

        for hero_line_number in range(len(bars_rectangles)):
            hero = self.create_hero(image,
                                    bars_rectangles[hero_line_number],
                                    rest_buttons_rectangles[hero_line_number],
                                    work_buttons_rectangles[hero_line_number])

            heroes.add(hero)

            self._logger.info('ID:' + hero.id + ' | EL:' + str(hero.energy_level))

        return heroes

    def create_hero(self, image, bar_rectangle, rest_rectangle, work_rectangle):
        hero = Hero(image, bar_rectangle, rest_rectangle, work_rectangle,
                    self._image_processor)

        return hero

    def update_first_hero_point(self, image):
        bars = self._image_processor.hero_bar(image)

        first_bar = bars.first_rectangle()

        self.set_hero_height(first_bar)

        x_bar, y_bar, w_bar, h_bar = first_bar
        self._first_hero_point = (x_bar, y_bar)

    def update_last_hero_point(self, point):
        x_bar, y_bar, w_bar, h_bar = point
        self._last_hero_point = (x_bar, y_bar + h_bar)

    def set_hero_height(self, rectangle):
        x_bar, y_bar, w_bar, h_bar = rectangle
        self._hero_height = h_bar