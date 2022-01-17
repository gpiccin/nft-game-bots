import platform
from random import uniform
import pyautogui

from src.logger import log


class ActionExecutor:

    @staticmethod
    def refresh_page():
        log('Refreshing')

        system = platform.system()

        if system == "Linux" or system == "Windows":
            pyautogui.hotkey('ctrl', 'f5')
            return

        pyautogui.hotkey('command', 'shift', 'R')

    @staticmethod
    def move_to(point):
        x, y = point
        pyautogui.moveTo(x, y, uniform(0.3, 0.7), pyautogui.easeOutQuad)
        return point

    @staticmethod
    def click(point):
        x, y = ActionExecutor.move_to(point)
        log('Click (' + str(x) + ',' + str(y) + ')')
        pyautogui.click()