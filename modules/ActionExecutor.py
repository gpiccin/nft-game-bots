import logging
import platform
import time
from random import uniform

import numpy
import pyautogui


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
    def _move_to(x, y):
        pyautogui.moveTo(x, y, duration=uniform(0.2, 0.5), logScreenshot=False)
        return (x, y)

    @staticmethod
    def click_rectangle(rectangle):
        x, y, width, height = rectangle

        position_x = x + width * uniform(0.1, 0.9)
        position_y = y + height * uniform(0.1, 0.9)

        ActionExecutor.click((position_x, position_y))

    @staticmethod
    def click(point):
        x, y = point

        x = int(numpy.trunc(x))
        y = int(numpy.trunc(y))

        ActionExecutor._move_to(x, y)
        logging.getLogger(__name__).debug('Click (' + str(x) + ',' + str(y) + ')')

        pyautogui.click()
