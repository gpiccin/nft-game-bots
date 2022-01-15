from src.date import formatted_date

import sys
import yaml

last_log_is_progress = False

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}


def log(message, progress_indicator=False, color='default'):
    global last_log_is_progress
    color_formatted = COLOR.get(color.lower(), COLOR['default'])

    formatted_datetime = formatted_date()
    formatted_message = "[{}] => {}".format(formatted_datetime, message)
    formatted_message_colored = color_formatted + formatted_message + '\033[0m'

    # Start progress indicator and append dots to in subsequent progress calls
    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            formatted_message = color_formatted + "[{}] => {}".format(formatted_datetime, '⬆️ Processing last action..')
            sys.stdout.write(formatted_message)
            sys.stdout.flush()
        else:
            sys.stdout.write(color_formatted + '.')
            sys.stdout.flush()
        return

    if last_log_is_progress:
        sys.stdout.write('\n')
        sys.stdout.flush()
        last_log_is_progress = False

    print(formatted_message_colored)

    return True


def log_new_map_click():
    log('🗺️ New Map button clicked!')
    logger_file = open("./logs/new-map.log", "a", encoding='utf-8')
    logger_file.write(formatted_date() + '\n')
    logger_file.close()
