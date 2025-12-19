import time
from utils import log

class Integrator:
    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.seen = set()
        self.artifact = {}

    def run(self, stop_event):
        log("Integrator START")
        while not stop_event.is_set():
            snapshot = self.blackboard.snapshot()
            for k, v in snapshot.items():
                if k not in self.seen:
                    self.seen.add(k)
                    self.artifact[k] = v
                    log(f"Integrator UPDATED artifact with [{k}]")
            time.sleep(0.05)
        log("Integrator STOP")
