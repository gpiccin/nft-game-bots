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

        # COLOR_BGR2HSV_FULL = 66
        #
        # COLOR_BGR2Lab = 44
        # COLOR_BGR2LAB = 44
        # COLOR_BGR2Luv = 50
        # COLOR_BGR2LUV = 50
        # COLOR_BGR2RGB = 4
        # COLOR_BGR2RGBA = 2
        # COLOR_BGR2XYZ = 32
        # COLOR_BGR2YCrCb = 36
        #
        # COLOR_BGR2YCR_CB = 36
        #
        # COLOR_BGR2YUV = 82
        #
        # COLOR_BGR2YUV_I420 = 128
        # COLOR_BGR2YUV_IYUV = 128
        # COLOR_BGR2YUV_YV12 = 132

        rgb_id_image = cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2RGB)
        gray_id_image = cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2GRAY)
        (thresh, black_and_white_id_image) = cv2.threshold(gray_id_image, 160, 255, cv2.THRESH_BINARY)

        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2Lab), 'COLOR_BGR2Lab')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2Luv), 'COLOR_BGR2Luv')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2LUV), 'COLOR_BGR2LUV')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2RGB), 'COLOR_BGR2RGB')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2RGBA), 'COLOR_BGR2RGBA')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2XYZ), 'COLOR_BGR2XYZ')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2YCrCb), 'COLOR_BGR2YCrCb')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2YCR_CB), 'COLOR_BGR2YCR_CB')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2YUV), 'COLOR_BGR2YUV')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2YUV_I420), 'COLOR_BGR2YUV_I420')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2YUV_IYUV), 'COLOR_BGR2YUV_IYUV')
        # ImageProcessor.show(cv2.cvtColor(hero_id_image, cv2.COLOR_BGR2YUV_YV12), 'COLOR_BGR2YUV_YV12')


        black_and_white_id_image_base64 = base64.b64encode(rgb_id_image)
        #ImageProcessor.show(rgb_id_image, 'Finding')
        #ImageProcessor.show(black_and_white_id_image, 'Black and white')

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
    def extract_hero_line_image(image, bar_rectangle: Rectangle, rest_rectangle: Rectangle):
        hero_line = ImageProcessor.cut_rectangles(image, bar_rectangle, rest_rectangle)
        return hero_line

    @staticmethod
    def extract_rest_button_image(image, rest_rectangle: Rectangle):
        rest_button = ImageProcessor.cut_rectangle(image, rest_rectangle)
        return rest_button

    @staticmethod
    def extract_id_image(image, bar_rectangle: Rectangle):
        # id_image = image[bar_rectangle.top:bar_rectangle.top + bar_rectangle.height,
        #
        #            bar_rectangle.left + bar_rectangle.width - 60:
        #            bar_rectangle.left + bar_rectangle.width + 2 + int(bar_rectangle.width * 28)]

        id_image = image[bar_rectangle.top + 6: bar_rectangle.top + 24,
                   bar_rectangle.left + bar_rectangle.width:
                   bar_rectangle.left + bar_rectangle.width + 80]


        return id_image

    @staticmethod
    def is_hero_energy_bar_green(energy_bar_image):
        color_found = ImageProcessor.dominant_color(energy_bar_image)
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