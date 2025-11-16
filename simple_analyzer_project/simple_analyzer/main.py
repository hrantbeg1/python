import time, random
from pathlib import Path
from .analyzer import Analyzer

CFG = Path(__file__).parent / "config" / "config.txt"

def read_cfg():
    vals = {"interval": 2, "sequence_length": 18}
    with open(CFG, "r") as f:
        for line in f:
            line=line.strip()
            if not line or "=" not in line:
                continue
            k,v = line.split("=",1)
            if k in ("interval","sequence_length"):
                vals[k] = int(v)
    print(f"Config -> interval={vals['interval']}, sequence_length={vals['sequence_length']}")
    return vals["interval"], vals["sequence_length"]

def main():
    interval, seq_len = read_cfg()
    A = Analyzer()
    while True:
        x = random.randint(1, 100)
        A.add_number(x)

        if len(A.data) > seq_len:
            A.data.pop(0)

        print(
            f"count={len(A.data)} | even={A.even_count()} | odd={A.odd_count()} "
            f"| max={A.highest_number()} | inc_pairs={A.increasing_pairs()}"
        )

        now = time.localtime()
        if len(A.data) >= seq_len and now.tm_sec == 0:
            print("Stopping condition reached.")
            break

        time.sleep(interval)

if __name__ == "__main__":
    main()
