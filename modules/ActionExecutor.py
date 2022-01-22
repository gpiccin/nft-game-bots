import platform
from random import uniform
import pyautogui

from logger import log


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
        pyautogui.moveTo(x, y, duration=uniform(0.2, 0.5), tween=pyautogui.easeOutQuad)
        return point

    @staticmethod
    def click_rectangle(rectangle):
        x, y, width, height = rectangle

        position_x = x + width * uniform(0.1, 0.9)
        position_y = y + height * uniform(0.1, 0.9)

        x, y = ActionExecutor.move_to((position_x, position_y))
        log('Click (' + str(x) + ',' + str(y) + ')')
        pyautogui.click()

    @staticmethod
    def click(point):
        x, y = ActionExecutor.move_to(point)
        log('Click (' + str(x) + ',' + str(y) + ')')
        pyautogui.click()