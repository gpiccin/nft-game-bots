import time

import re

import numpy as np
import pyautogui
import pytesseract

from src.bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from src.bombcrypto.Hero import Hero
from src.logger import log
from src.modules.ActionExecutor import ActionExecutor
from src.modules.ImageProcessor import ImageProcessor


class GreenBarStrategy:
    def __init__(self, bomb_crypto_image_processor: BombCryptoImageProcessor):
        self._image_processor = bomb_crypto_image_processor
        self._hero_height = 0
        self._last_hero_point = None
        self._first_hero_point = None
        self._heroes_analyzed = 0
        self.heroes = {}

    def run(self, image):
        if not self._image_processor.is_in_the_heroes_screen(image):
            return

        self.heroes = {}

        self.scroll_up_heroes_list(image)

        self.load_heroes(self._image_processor.image())
        self.scroll_down_heroes_list()
        self.load_heroes(self._image_processor.image())
        self.scroll_down_heroes_list()
        self.load_heroes(self._image_processor.image())

        log(len(self.heroes))
        a = 1

    def scroll_up_heroes_list(self, image):
        self.update_first_hero_point(image)

        x, y = self._first_hero_point
        #ActionExecutor.click(self._first_hero_point)
        ActionExecutor.click(self._first_hero_point)
        #pyautogui.scroll(self._hero_height * 5.3, x=x, y=y)
        pyautogui.dragRel(yOffset=self._hero_height * 15, duration=0.3,
                           button='left')
        time.sleep(0.5)

    def scroll_down_heroes_list(self):
        ActionExecutor.click(self._last_hero_point)
        ActionExecutor.click(self._last_hero_point)
        pyautogui.dragRel(0, -self._hero_height * 5.25, duration=1,
                          button='left')
        time.sleep(2)

    def load_heroes(self, image):
        bars = self._image_processor.hero_localization_bar(image)
        rest_buttons = self._image_processor.rest(image)

        # self._image_processor.debug_image(image, [bars, rest_buttons])

        bars_rectangles = bars.rectangles()
        rest_buttons_rectangles = rest_buttons.rectangles()

        self.update_last_hero_point(bars_rectangles[len(bars_rectangles) -1 ])

        #rgb(252, 149, 29)

        for hero_line_number in range(len(bars_rectangles)):
            x, y, w, h = rest_buttons_rectangles[hero_line_number]

            debug_image = image.copy()
            ImageProcessor.draw_circle(debug_image, (x+2, y+2))
            #ImageProcessor.show(debug_image)


            hero = self.get_hero(image,
                                 bars_rectangles[hero_line_number],
                                 rest_buttons_rectangles[hero_line_number])

            self.heroes[hero.id] = hero

    def get_hero(self, image, bar_rectangle, rest_rectangle):
        x_bar, y_bar, w_bar, h_bar = bar_rectangle
        x_rest, y_rest, w_rest, h_rest = rest_rectangle

        hero_line_image = image[y_bar:y_bar + h_bar, x_bar:x_bar + x_rest - x_bar + w_rest]
        hero_id_image = image[y_bar:y_bar + int(h_bar / 2), x_bar + w_bar + 2:x_bar + w_bar + 2 + int(w_bar * 9.8)]

        is_resting = pyautogui.pixelMatchesColor(x_rest + 4, y_rest + 4, (252, 149, 29), tolerance=30)
        # ImageProcessor.show(hero_id_image)

        hero = Hero(hero_id_image,
                    hero_line_image,
                    self._image_processor, is_resting)

        return hero

    def update_first_hero_point(self, image):
        bars = self._image_processor.hero_localization_bar(image)

        first_bar = bars.rectangles()[0]

        self.set_hero_height(first_bar)

        x_bar, y_bar, w_bar, h_bar = first_bar
        self._first_hero_point = (x_bar, y_bar)

    def update_last_hero_point(self, point):
        x_bar, y_bar, w_bar, h_bar = point
        self._last_hero_point = (x_bar, y_bar + h_bar)

    def set_hero_height(self, rectangle):
        x_bar, y_bar, w_bar, h_bar = rectangle
        self._hero_height = h_bar
