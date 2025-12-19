import threading

class Blackboard:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def write(self, key, value):
        with self._lock:
            self._data[key] = value

    def snapshot(self):
        with self._lock:
            return dict(self._data)
