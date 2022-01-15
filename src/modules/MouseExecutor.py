from random import random

import pyautogui


class MouseExecutor:

    @staticmethod
    def click(point, movement_duration=1):
        x, y = point
        pyautogui.moveTo(x, y, movement_duration + random() / 2)
        pyautogui.click()