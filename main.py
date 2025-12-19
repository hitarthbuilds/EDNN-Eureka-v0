import threading
import time

from agent import Agent
from blackboard import Blackboard
from integrator import Integrator
from utils import log

def structure_task():
    return {"folders": ["src/", "tests/", "README.md"]}

def code_task():
    return {"src/main.py": "print('hello')"}

def main():
    blackboard = Blackboard()
    stop_event = threading.Event()

    integrator = Integrator(blackboard)
    integrator_thread = threading.Thread(
        target=integrator.run,
        args=(stop_event,),
        daemon=True
    )
    integrator_thread.start()

    agents = [
        Agent("structure", 1.0, structure_task),
        Agent("code", 3.0, code_task),
    ]

    threads = []
    for agent in agents:
        t = threading.Thread(target=agent.run, args=(blackboard,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    time.sleep(0.5)
    stop_event.set()
    time.sleep(0.1)

    log(f"FINAL ARTIFACT: {integrator.artifact}")

if __name__ == "__main__":
    main()
