import logging
import platform
import time
from random import uniform

import numpy
import pyautogui

from modules.Rectangle import Rectangle


class ActionExecutor:

    @staticmethod
    def refresh_page():
        logging.getLogger(__name__).debug('Refreshing')

        system = platform.system()

        if system == "Linux" or system == "Windows":
            pyautogui.hotkey('f5')
            time.sleep(5)
            return

        pyautogui.hotkey('command', 'shift', 'R')

    @staticmethod
    def maximize():
        logging.getLogger(__name__).debug('Maximizing')

        system = platform.system()

        if system == "Linux" or system == "Windows":
            pyautogui.hotkey('f5')
            time.sleep(5)
            return

        pyautogui.hotkey('command', 'ctrl', '=')

    @staticmethod
    def _move_to(x, y):
        pyautogui.moveTo(x, y, duration=uniform(0.1, 0.3), logScreenshot=False)
        return x, y

    @staticmethod
    def click_rectangle(rectangle: Rectangle):
        ActionExecutor.click(rectangle.random_point())

    @staticmethod
    def click(point):
        x, y = point

        x = int(numpy.trunc(x))
        y = int(numpy.trunc(y))

        ActionExecutor._move_to(x, y)
        logging.getLogger(__name__).debug('Click (' + str(x) + ',' + str(y) + ')')

        pyautogui.click()
