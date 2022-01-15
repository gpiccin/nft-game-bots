import time


class TimeControl:
    def __init__(self, seconds_to_expire=1):
        self._seconds_to_expire = seconds_to_expire
        self._init = time.time()
        self._last_execution = 0

    def is_running(self):
        return self._last_execution != 0

    def start(self):
        self._last_execution = time.time()

    def set_seconds_to_expire(self, seconds):
        self._seconds_to_expire = seconds

    def expire(self):
        self._last_execution = 0

    def elapsed_time(self):
        return time.time() - self._last_execution

    def is_expired(self):
        return not self.is_running() or self.elapsed_time() > self._seconds_to_expire
