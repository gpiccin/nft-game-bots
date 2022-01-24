import logging
import math
import platform
from random import uniform

import numpy
import numpy as np
import pyautogui


class ActionExecutor:

    @staticmethod
    def refresh_page():
        logging.getLogger(__name__).debug('Refreshing')

        system = platform.system()

        if system == "Linux" or system == "Windows":
            pyautogui.hotkey('f5')
            return

        pyautogui.hotkey('command', 'shift', 'R')

    @staticmethod
    def move_to(x, y):
        pyautogui.moveTo(math.trunc(x), math.trunc(y), duration=uniform(0.2, 0.5), logScreenshot=False)
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

        if x is numpy.int32:
            x = np.trunc(x)
        else:
            x = math.trunc(x)

        if y is numpy.int32:
            y = np.trunc(y)
        else:
            y = math.trunc(y)

        ActionExecutor.move_to(x, y)
        logging.getLogger(__name__).debug('Click (' + str(x) + ',' + str(y) + ')')

        pyautogui.click()
