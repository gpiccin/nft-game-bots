import time


def formatted_date(date_format='%Y-%m-%d %H:%M:%S'):
    datetime = time.localtime()
    formatted = time.strftime(date_format, datetime)
    return formatted
