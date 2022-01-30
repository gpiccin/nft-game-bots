import base64
import hashlib
import logging

import cv2

from bombcrypto.BombCryptoImageProcessor import BombCryptoImageProcessor
from modules.ImageProcessor import ImageProcessor
from modules.Rectangle import Rectangle


class Hero:
    UNKNOWN_ENERGY = 0
    FULL_ENERGY = 3
    GREEN_ENERGY = 2
    RED_ENERGY = 1

    def __init__(self, image,
                 bar_rectangle,
                 work_rectangle,
                 rest_rectangle,
                 image_processor: BombCryptoImageProcessor):

        self._logger = logging.getLogger(type(self).__name__)
        self._image = image
        self._bar_rectangle = bar_rectangle
        self._rest_rectangle = rest_rectangle
        self._work_rectangle = work_rectangle
        self._image_processor = image_processor

        self.id = None
        self.id_image = None
        self.type = type
        self.energy_level = None
        self.is_resting = None

        self._set_state()
        self._set_id()
        self._set_energy()

    def work_rectangle(self):
        return self._work_rectangle

    def _set_state(self):
        rest_button_image = Hero.extract_rest_button_image(self._image, self._rest_rectangle)
        self.is_resting = Hero.is_hero_resting(rest_button_image)

    def _set_id(self):
        hero_id_image = Hero.extract_id_image(self._image, self._bar_rectangle)
        rgb_id_image = cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2RGB)

        self.id = hashlib.md5(rgb_id_image).hexdigest()
        self.id_image = rgb_id_image

    def _set_energy(self):
        hero_line_image = Hero.extract_hero_line_image(self._image, self._bar_rectangle, self._rest_rectangle)
        energy_bar = self._image_processor.full_bar(hero_line_image)

        if energy_bar:
            self.energy_level = Hero.FULL_ENERGY
            return

        energy_bar_image = Hero.extract_energy_bar_image(self._image_processor, hero_line_image)

        if Hero.is_hero_energy_bar_green(energy_bar_image):
            self.energy_level = Hero.GREEN_ENERGY
            return

        self.energy_level = Hero.RED_ENERGY

    @staticmethod
    def extract_energy_bar_image(image_processor: BombCryptoImageProcessor, hero_line_image):
        begin_energy_bar = image_processor.begin_energy_bar(hero_line_image)
        end_energy_bar = image_processor.end_energy_bar(hero_line_image)

        begin_energy_bar_rect = begin_energy_bar.first_rectangle()
        end_energy_bar_rect = end_energy_bar.first_rectangle()

        energy_bar_image = ImageProcessor.cut_rectangles(hero_line_image, begin_energy_bar_rect, end_energy_bar_rect)

        return energy_bar_image

    @staticmethod
    def extract_half_of_energy_bar_image(energy_bar_image):
        width = energy_bar_image.shape[1]
        height = energy_bar_image.shape[0]
        return energy_bar_image[0: height, 0:int(width / 2)]

    @staticmethod
    def extract_hero_line_image(image, bar_rectangle: Rectangle, rest_rectangle: Rectangle):
        hero_line = ImageProcessor.cut_rectangles(image, bar_rectangle, rest_rectangle)
        return hero_line

    @staticmethod
    def extract_rest_button_image(image, rest_rectangle: Rectangle):
        rest_button = ImageProcessor.cut_rectangle(image, rest_rectangle)
        return rest_button

    @staticmethod
    def extract_id_image(image, bar_rectangle: Rectangle):
        id_image = image[bar_rectangle.top + 6: bar_rectangle.top + 24,
                   bar_rectangle.left + bar_rectangle.width:
                   bar_rectangle.left + bar_rectangle.width + 80]

        return id_image

    @staticmethod
    def is_hero_energy_bar_green(energy_bar_image):
        half_energy_bar = Hero.extract_half_of_energy_bar_image(energy_bar_image)
        color_found = ImageProcessor.dominant_color(half_energy_bar)
        list_of_colors = [[192, 151, 127], [176, 167, 127]]
        closest_color = ImageProcessor.closest_color(list_of_colors, color_found)
        return closest_color[0][1] == 167

    @staticmethod
    def is_hero_resting(rest_button_image):
        color_found = ImageProcessor.dominant_color(rest_button_image)
        color = [color_found[0], color_found[1], color_found[2]]
        list_of_colors = [[169, 124, 79], [221, 158, 93]]
        closest_color = ImageProcessor.closest_color(list_of_colors, color)
        return closest_color[0][0] == 221
