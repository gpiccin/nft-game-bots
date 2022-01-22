import re
import time
import uuid

import pyautogui
from pytesseract import pytesseract

from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from logger import log
from modules.ActionExecutor import ActionExecutor
from modules.ImageProcessor import ImageProcessor


class HeroesReader:
    def __init__(self, image_processor: BombCryptoImageProcessor):
        self._last_hero_point = None
        self._first_hero_point = None
        self._hero_height = None
        self._image_processor = image_processor
        self.heroes = {}

    def scroll_up_heroes_list(self, image=None):
        if image is None:
            image = self._image_processor.image()

        self.update_first_hero_point(image)

        ActionExecutor.click(self._first_hero_point)
        ActionExecutor.click(self._first_hero_point)

        pyautogui.dragRel(yOffset=self._hero_height * 15, duration=0.3,
                          button='left')
        time.sleep(0.5)

    def scroll_down_heroes_list(self):
        ActionExecutor.click(self._last_hero_point)
        ActionExecutor.click(self._last_hero_point)
        pyautogui.dragRel(0, -self._hero_height * 6, duration=1,
                          button='left')
        time.sleep(2)

    def load_all_heroes(self, image):
        self.update_first_hero_point(image)

        heroes = dict(self._load_heroes(image))

        if len(heroes) == 5:
            self.scroll_down_heroes_list()
            new_heroes = self._load_heroes(self._image_processor.image())

            if new_heroes is not None:
                heroes.update(new_heroes)

        if len(heroes) == 10:
            self.scroll_down_heroes_list()
            new_heroes = self._load_heroes(self._image_processor.image())

            if new_heroes is not None:
                heroes.update(new_heroes)

        self.heroes = heroes

        log('Heroes found: ' + str(len(heroes)))

        for h_id in heroes.keys():
            log('Hero: ' + h_id)

        return heroes

    def find_hero(self, image, id):
        heroes = self._load_heroes(image)

        if self.contains_hero(heroes, id):
            return heroes[id]

        self.scroll_up_heroes_list()
        heroes = dict(self._load_heroes(self._image_processor.image()))

        if self.contains_hero(heroes, id):
            return heroes[id]

        if len(heroes) == 5:
            self.scroll_down_heroes_list()
            heroes.update(self._load_heroes(self._image_processor.image()))

        if self.contains_hero(heroes, id):
            return heroes[id]

        if len(heroes) == 10:
            self.scroll_down_heroes_list()
            heroes.update(self._load_heroes(self._image_processor.image()))

        if self.contains_hero(heroes, id):
            return heroes[id]

        return None

    @staticmethod
    def contains_hero(heroes, id):
        return heroes.get(id) is not None

    def _load_heroes(self, image=None) -> {}:
        if image is None:
            image = self._image_processor.image()

        bars = self._image_processor.hero_bar(image)
        work_buttons = self._image_processor.work(image)
        rest_buttons = self._image_processor.rest(image)

        # self._image_processor.debug_image(image, [bars, rest_buttons])

        if bars is None or work_buttons is None or rest_buttons is None:
            return

        bars_rectangles = bars.rectangles()
        work_buttons_rectangles = work_buttons.rectangles()
        rest_buttons_rectangles = rest_buttons.rectangles()

        if len(bars_rectangles) != len(work_buttons_rectangles) or \
            len(bars_rectangles) != len(rest_buttons_rectangles) or \
            len(work_buttons_rectangles) != len(rest_buttons_rectangles):
            return

        heroes = {}

        self.update_last_hero_point(bars_rectangles[len(bars_rectangles) - 1])

        for hero_line_number in range(len(bars_rectangles)):
            hero = self.create_hero(image,
                                    bars_rectangles[hero_line_number],
                                    rest_buttons_rectangles[hero_line_number],
                                    work_buttons_rectangles[hero_line_number])

            heroes[hero.id] = hero

        return heroes

    def create_hero(self, image, bar_rectangle, rest_rectangle, work_rectangle):
        hero = Hero(image, bar_rectangle, rest_rectangle, work_rectangle,
                    self._image_processor, self)

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


class Hero:
    UNKNOWN_ENERGY = 0
    FULL_ENERGY = 3
    GREEN_ENERGY = 2
    RED_ENERGY = 1

    def __init__(self, image,
                 bar_rectangle, rest_rectangle,
                 work_rectangle,
                 image_processor: BombCryptoImageProcessor,
                 heroes_reader: HeroesReader):

        self._heroes_header = heroes_reader
        self._image = image
        self._bar_rectangle = bar_rectangle
        self._rest_rectangle = rest_rectangle
        self._work_rectangle = work_rectangle
        self.id = None
        self.type = type
        self.energy_level = None
        self._image_processor = image_processor
        self._set_hero_information(bar_rectangle,
                                   rest_rectangle)

    def get_work_rectangle(self):
        return self._work_rectangle

    def send_to_work(self, image):
        if not self.is_resting:
            return

        hero = self._heroes_header.find_hero(image, self.id)

        if hero is None:
            return

        ActionExecutor.click_rectangle(hero.get_work_rectangle())
        time.sleep(0.5)

    def _set_hero_information(self,
                              bar_rectangle, rest_rectangle):

        x_bar, y_bar, w_bar, h_bar = bar_rectangle
        x_rest, y_rest, w_rest, h_rest = rest_rectangle

        hero_line_image = self._image[y_bar:y_bar + h_bar,
                          x_bar:x_bar + x_rest - x_bar + w_rest]

        hero_id_image = self._image[y_bar:y_bar + int(h_bar / 2),
                        x_bar + w_bar + 2:x_bar + w_bar + 2 + int(w_bar * 9.8)]

        # ImageProcessor.show(hero_line_image)

        self._set_id(hero_id_image)
        self._set_energy(hero_line_image)
        self._set_state(self._image[y_rest:y_rest + h_rest, x_rest:x_rest + w_rest])

    def _set_state(self, image):
        color_found = ImageProcessor.dominant_color(image)
        color = [color_found[0], color_found[1], color_found[2]]

        list_of_colors = [[169, 124, 79], [221, 158, 93]]
        closest_color = ImageProcessor.closest_color(list_of_colors, color)

        self.is_resting = closest_color[0][0] == 221

    def _set_id(self, id_image):
        id_text = pytesseract.image_to_string(id_image)
        id_text = re.findall(r'\d+', id_text)

        if len(id_text) > 0:
            self.id = id_text[0]
        else:
            self.id = str(uuid.uuid1())

        self._id_image = id_image

    def _set_energy(self, hero_line_image):
        energy_bar = self._image_processor.full_bar(hero_line_image)

        if energy_bar:
            self.energy_level = Hero.FULL_ENERGY
            return

        energy_bar_image = self._get_energy_bar_image(hero_line_image)

        if Hero._is_green_energy_bar(energy_bar_image):
            self.energy_level = Hero.GREEN_ENERGY
            return

        self.energy_level = Hero.RED_ENERGY

    def _get_energy_bar_image(self, hero_line_image):
        begin_energy_bar = self._image_processor.begin_energy_bar(hero_line_image)
        end_energy_bar = self._image_processor.end_energy_bar(hero_line_image)

        x_begin_energy_bar, y_begin_energy_bar, \
        w_begin_energy_bar, h_begin_energy_bar = \
            begin_energy_bar.first_rectangle()

        x_end_energy_bar, y_end_energy_bar, \
        w_end_energy_bar, h_end_energy_bar = \
            end_energy_bar.first_rectangle()

        image = hero_line_image[y_begin_energy_bar:y_begin_energy_bar + h_end_energy_bar,
                x_begin_energy_bar:x_end_energy_bar + w_end_energy_bar]

        return image

    @staticmethod
    def _is_green_energy_bar(image):
        color_found = ImageProcessor.dominant_color(image)
        list_of_colors = [[192, 151, 127], [176, 167, 127]]
        closest_color = ImageProcessor.closest_color(list_of_colors, color_found)
        return closest_color[0][1] == 167
