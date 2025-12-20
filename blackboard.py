class Blackboard:
    def __init__(self):
        self.storage = {}

    def write(self, key, value):
        self.storage[key] = value

    def read_all(self):
        return self.storage
