import time
from utils import log

class Agent:
    def __init__(self, name, duration, payload_fn):
        self.name = name
        self.duration = duration
        self.payload_fn = payload_fn

    def run(self, blackboard):
        log(f"Agent {self.name} START")
        time.sleep(self.duration)
        result = self.payload_fn()
        blackboard.write(self.name, result)
        log(f"Agent {self.name} END (wrote result)")
