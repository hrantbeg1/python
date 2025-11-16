from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data.txt"

class Tracker:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def save_to_file(self):
        with open(DATA_FILE, "w") as f:
            f.write(str(self.count))

    def reset(self):
        self.count = 0

    def __str__(self):
        return f"Current count: {self.count}"
