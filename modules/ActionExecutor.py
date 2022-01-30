import logging
import platform
import time
from random import uniform

import numpy
import pyautogui


class ActionExecutor:

    @staticmethod
    def drag(xOffset=0, yOffset=0, duration=0.0):
        pyautogui.drag(xOffset, yOffset, duration=duration, button='left')

    @staticmethod
    def refresh_page():
        logging.getLogger(__name__).debug('Refresh browser')

        system = platform.system()

        if system == "Linux" or system == "Windows":
            pyautogui.hotkey('f5')
            time.sleep(5)
            return

        pyautogui.hotkey('command', 'shift', 'R')

    @staticmethod
    def maximize():
        logging.getLogger(__name__).debug('Maximize')

        system = platform.system()

        if system == "Windows":
            pyautogui.hotkey('f11')
            return

        if system == "Linux":
            pyautogui.hotkey('alt', 'f10')
            return

        pyautogui.hotkey('command', 'ctrl', '=')

    @staticmethod
    def click(point):
        x, y = point

        x = int(numpy.trunc(x))
        y = int(numpy.trunc(y))

        pyautogui.moveTo(x, y, duration=uniform(0.1, 0.3), logScreenshot=False)

        logging.getLogger(__name__).debug('Click (' + str(x) + ',' + str(y) + ')')
        pyautogui.click()
