import time

START_TIME = time.time()

def log(msg):
    t = time.time() - START_TIME
    print(f"[t={t:6.2f}s] {msg}")
