import logging
import math
import platform
from random import uniform
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
    def move_to(point):
        x, y = point
        pyautogui.moveTo(math.trunc(x), math.trunc(y), duration=uniform(0.2, 0.5), logScreenshot=False)
        return point

    @staticmethod
    def click_rectangle(rectangle):
        x, y, width, height = rectangle

        position_x = x + width * uniform(0.1, 0.9)
        position_y = y + height * uniform(0.1, 0.9)

        ActionExecutor.click((position_x, position_y))

    @staticmethod
    def click(point):
        ActionExecutor.move_to(point)

        x, y = point
        logging.getLogger(__name__).debug('Click (' + str(x) + ',' + str(y) + ')')

        pyautogui.click()