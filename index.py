# -*- coding: utf-8 -*-    
from src.logger import log, log_new_map_click
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
import mss
import pyautogui
import time
import sys
import yaml

# Load config file.
stream = open("config.yaml", 'r')
config = yaml.safe_load(stream)
threshold_config = config['threshold']
home_config = config['home']
seconds_between_movements = config['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = seconds_between_movements

test_image_name = 'connect_wallet'

cat = """
                                                _
                                                \`*-.
                                                 )  _`-.
                                                .  : `. .
                                                : _   '  \\
                                                ; *` _.   `*-._
                                                `-.-'          `-.
                                                  ;       `       `.
                                                  :.       .        \\
                                                  . \  .   :   .-'   .
                                                  '  `+.;  ;  '      :
                                                  :  '  |    ;       ;-.
                                                  ; '   : :`-:     _.`* ;
                                               .*' /  .*' ; .*`- +'  `*'
                                               `*-*   `*-*  `*-*'
=========================================================================
========== 💰 Have I helped you in any way? All I ask is a tip! 🧾 ======
========== ✨ Faça sua boa ação de hoje, manda aquela gorjeta! 😊 =======
=========================================================================
======================== vvv BCOIN BUSD BNB vvv =========================
============== 0xbd06182D8360FB7AC1B05e871e56c76372510dDf ===============
=========================================================================
===== https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ ======
=========================================================================

>>---> Press ctrl + config to kill the bot.

>>---> Some configs can be found in the config.yaml file."""


def get_randomized_integer(value, random_factor_size=None):
    """Returns n with randomness
    Parameters:
        value (int): A decimal integer
        random_factor_size (int): The maximum value+- of randomness that will be
            added to n

    Returns:
        int: n with randomness
    """

    if random_factor_size is None:
        randomness_percentage = 0.1
        random_factor_size = randomness_percentage * value

    random_factor = 2 * random() * random_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = value - random_factor_size
    randomized_number = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.date_format(int(value), randomized_number))
    return int(randomized_number)


def move_mouse_to(x, y, movement_duration):
    pyautogui.moveTo(get_randomized_integer(x, 10), get_randomized_integer(y, 10), movement_duration + random() / 2)


def remove_suffix(input_string, suffix):
    """Returns the input_string without the extension"""

    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]

    return input_string


def load_target_images(dir_path='./targets/'):
    """ Programmatically loads all target_images of dir_path as a key:value where the
        key is the file name without the .png extension

    Returns:
        dict: dictionary containing the loaded target_images as key:value pairs.
    """

    file_names = listdir(dir_path)
    targets = {}

    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets


def load_test_images(dir_path='./test-_image_names/'):
    """ Programmatically loads all target_images of dir_path as a key:value where the
        key is the file name without the .png extension

    Returns:
        dict: dictionary containing the loaded target_images as key:value pairs.
    """

    file_names = listdir(dir_path)
    targets = {}

    for file in file_names:
        path = 'test-_image_names/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets


def load_heroes():
    """Loads the target_images in the path and saves them as a list"""
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        heroes.append(cv2.imread(path))

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes


def show_rectangle(rectangles, img=None):
    """ Show an popup with rectangles showing the rectangles[(x, y, w, h),...]
        over target_image or a printSreen if no target_image provided. Useful for debugging"""

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255, 255), 2)

    cv2.imshow('target_image', img)
    cv2.waitKey(0)


def click_button(target_image, timeout=3, threshold=threshold_config['default']):
    """Search for image in the scree, if found moves the cursor over it and clicks.
    Parameters:
        target_image: The image that will be used as an template to find where to click.
        timeout (int): Time in seconds that it will keep looking for the image before returning with fail
        threshold(float): How confident the bot needs to be to click the buttons (values from 0 to 1)
    """

    log(None, progress_indicator=True)
    start = time.time()
    has_timed_out = False
    while not has_timed_out:
        image = print_screen()

        matches = get_target_image_positions(target_image, threshold=threshold, image=image)

        if len(matches) == 0:
            has_timed_out = time.time() - start > timeout
            continue

        show_rectangle(matches, image)

        x, y, width, height = matches[0]
        pos_click_x = x + width / 2
        pos_click_y = y + height / 2
        move_mouse_to(pos_click_x, pos_click_y, 1)
        pyautogui.click()
        return True

    return False


def print_screen():
    if test_image_name:
        test_image = load_test_images()
        return test_image[test_image_name]

    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:, :, :3]


def get_target_image_positions(target_image, threshold=threshold_config['default'], image=None):
    if image is None:
        image = print_screen()

    result = cv2.matchTemplate(image, target_image, cv2.TM_CCOEFF_NORMED)

    width = target_image.shape[1]
    height = target_image.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(width), int(height)])
        rectangles.append([int(x), int(y), int(width), int(height)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def scroll():
    commons = get_target_image_positions(target_images['commom-text'], threshold=threshold_config['commom'])

    if len(commons) == 0:
        return

    x, y, w, h = commons[len(commons) - 1]
    move_mouse_to(x, y, 1)

    if not config['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-config['scroll_size'])
    else:
        pyautogui.dragRel(0, -config['click_and_drag_amount'], duration=1, button='left')


def send_all_heroes_to_work():
    buttons = get_target_image_positions(target_images['go-work'], threshold=threshold_config['go_to_work_btn'])
    # print('buttons: {}'.date_format(len(buttons)))

    for (x, y, width, height) in buttons:
        move_mouse_to(x + (width / 2), y + (height / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            log('too many hero clicks, try to increase the go_to_work_btn threshold')
            return

    return len(buttons)


def is_home(hero, buttons):
    y = hero[1]

    for (_, button_y, _, button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True


def is_hero_working(bar, buttons):
    y = bar[1]

    for (_, button_y, _, button_h) in buttons:
        is_below = y < (button_y + button_h)
        is_above = y > (button_y - button_h)

        if is_below and is_above:
            return False

    return True


def send_hero_with_green_bar_to_work():
    offset = 140

    green_bars = get_target_image_positions(target_images['green-bar'], threshold=threshold_config['green_bar'])
    log('🟩 %d green bars detected' % len(green_bars))

    buttons = get_target_image_positions(target_images['go-work'], threshold=threshold_config['go_to_work_btn'])
    log('🆗 %d buttons detected' % len(buttons))

    not_working_green_bars = []

    for bar in green_bars:
        if not is_hero_working(bar, buttons):
            not_working_green_bars.append(bar)

    if len(not_working_green_bars) > 0:
        log('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        log('👆 Clicking in %d heroes' % len(not_working_green_bars))

    clicked_heroes = 0

    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        move_mouse_to(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()

        global hero_clicks
        hero_clicks = hero_clicks + 1
        clicked_heroes = clicked_heroes + 1

        if clicked_heroes > 20:
            log('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return

        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)


def send_hero_with_full_green_bar_to_work():
    offset = 100

    full_bars = get_target_image_positions(target_images['full-stamina'], threshold=threshold_config['default'])
    buttons = get_target_image_positions(target_images['go-work'], threshold=threshold_config['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not is_hero_working(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        log('👆 Clicking in %d heroes' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        move_mouse_to(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)


def go_to_heroes_screen():
    if click_button(target_images['go-back-arrow']):
        global login_attempts
        login_attempts = 0

    time.sleep(1)
    click_button(target_images['hero-icon'])
    time.sleep(randint(1, 3))


def go_to_game():
    # in case of server overload popup
    click_button(target_images['x'])
    # time.sleep(3)
    click_button(target_images['x'])

    click_button(target_images['treasure-hunt-icon'])


def refresh_heroes_position():
    log('🔃 Refreshing SendHeroesToWork Positions')
    click_button(target_images['go-back-arrow'])
    click_button(target_images['treasure-hunt-icon'])

    # time.sleep(3)
    click_button(target_images['treasure-hunt-icon'])


def login():
    global login_attempts
    log('😿 Checking if game has disconnected')

    if login_attempts > 3:
        log('🔃 Too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.hotkey('ctrl', 'f5')
        return

    if click_button(target_images['connect-wallet'], timeout=10):
        log('🎉 Connect wallet button detected, logging in!')
        login_attempts = login_attempts + 1
        # time.sleep(10)

    if click_button(target_images['select-wallet-2'], timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.date_format(login_attempts))
        if click_button(target_images['treasure-hunt-icon'], timeout=15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        return
        # click ok button

    if not click_button(target_images['select-wallet-1-no-hover'], ):
        if click_button(target_images['select-wallet-1-hover'], threshold=threshold_config['select_wallet_buttons']):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if click_button(target_images['select-wallet-2'], timeout=20):
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.date_format(login_attempts))
        # time.sleep(25)
        if click_button(target_images['treasure-hunt-icon'], timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if click_button(target_images['ok'], timeout=5):
        pass
        # time.sleep(15)
        # print('ok button clicked')


def send_heroes_to_home():
    if not home_config['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = get_target_image_positions(hero, threshold=home_config['hero_threshold'])
        if not len(hero_positions) == 0:
            # TODO maybe pick up match with most wheight instead of first
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = get_target_image_positions(target_images['send-home'],
                                                 threshold=home_config['home_button_threshold'])
    # TODO pass it as an argument for both this and the other function that uses it
    go_work_buttons = get_target_image_positions(target_images['go-work'], threshold=threshold_config['go_to_work_btn'])

    for position in heroes_positions:
        if not is_home(position, go_home_buttons):
            print(is_hero_working(position, go_work_buttons))
            if (not is_hero_working(position, go_work_buttons)):
                print('hero not working, sending him home')
                move_mouse_to(go_home_buttons[0][0] + go_home_buttons[0][2] / 2, position[1] + position[3] / 2,
                              1)
                pyautogui.click()
            else:
                print('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')


def send_heroes_to_work():
    log('🏢 Search for heroes to work')

    go_to_heroes_screen()

    if config['select_heroes_mode'] == "full":
        log('⚒️ Sending heroes with full stamina bar to work', 'green')
    elif config['select_heroes_mode'] == "green":
        log('⚒️ Sending heroes with green stamina bar to work', 'green')
    else:
        log('⚒️ Sending all heroes to work', 'green')

    buttonsClicked = 1
    empty_scrolls_attempts = config['scroll_attemps']

    while (empty_scrolls_attempts > 0):
        if config['select_heroes_mode'] == 'full':
            buttonsClicked = send_hero_with_full_green_bar_to_work()
        elif config['select_heroes_mode'] == 'green':
            buttonsClicked = send_hero_with_green_bar_to_work()
        else:
            buttonsClicked = send_all_heroes_to_work()

        send_heroes_to_home()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    log('💪 {} heroes sent to work'.format(hero_clicks))
    go_to_game()


def main():
    """Main execution setup and loop"""
    # ==Setup==
    global hero_clicks
    global login_attempts
    global last_log_is_progress
    hero_clicks = 0
    login_attempts = 0
    last_log_is_progress = False

    global target_images
    target_images = load_target_images()

    if home_config['enable']:
        global home_heroes
        home_heroes = load_heroes()
    else:
        print('>>---> Home feature not enabled')

    print('\n')

    # print(cat)
    time.sleep(7)
    time_intervals_config = config['time_intervals']

    last = {
        "login": 0,
        "heroes": 0,
        "new_map": 0,
        "check_for_captcha": 0,
        "refresh_heroes": 0
    }
    # =========

    while True:
        now = time.time()

        if now - last["check_for_captcha"] > get_randomized_integer(time_intervals_config['check_for_captcha'] * 60):
            last["check_for_captcha"] = now

        if now - last["heroes"] > get_randomized_integer(time_intervals_config['send_heroes_for_work'] * 60):
            last["heroes"] = now
            # send_heroes_to_work()

        # if now - last["login"] > get_randomized_integer(time_intervals_config['check_for_login'] * 60):
        sys.stdout.flush()
        last["login"] = now
        login()

        if now - last["new_map"] > time_intervals_config['check_for_new_map_button']:
            last["new_map"] = now

            if click_button(target_images['new-map']):
                log_new_map_click()

        if now - last["refresh_heroes"] > get_randomized_integer(time_intervals_config['refresh_heroes_positions'] * 60):
            last["refresh_heroes"] = now
            refresh_heroes_position()

        log(None, progress_indicator=True)

        sys.stdout.flush()

        time.sleep(1)


if __name__ == '__main__':
    main()

# cv2.imshow('target_image',sct_img)
# cv2.waitKey()
