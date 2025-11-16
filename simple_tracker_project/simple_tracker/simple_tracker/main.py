import time
from pathlib import Path
from .tracker import Tracker

CFG_PATH = Path(__file__).parent / "config" / "config.txt"

def read_interval():
    interval = 2
    with open(CFG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("interval="):
                interval = int(line.split("=", 1)[1])
    return interval

def main():
    interval = read_interval()
    t = Tracker()
    while True:
        t.increment()
        print("[tracker]", t)
        t.save_to_file()
        time.sleep(interval)

if __name__ == "__main__":
    main()
