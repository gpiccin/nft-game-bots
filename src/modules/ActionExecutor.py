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
    def click(point):
        x, y = point
        log('Click (' + str(x) + ',' + str(y) + ')')
        pyautogui.moveTo(x, y, uniform(0.3, 0.7), pyautogui.easeOutQuad)
        pyautogui.click()