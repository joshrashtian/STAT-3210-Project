import sys
import time
from pathlib import Path

CHUNK = 65536
WARMUP = 3


def read_file(path: Path) -> int:
    total = 0
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK):
            total += len(chunk)
    return total


def main():
    if len(sys.argv) < 3:
        sys.exit(f"usage: {sys.argv[0]} <file> <iterations>")

    path = Path(sys.argv[1])
    iterations = int(sys.argv[2])
    if iterations <= 0:
        sys.exit("iterations must be > 0")

    size = 0
    for _ in range(WARMUP):  # untimed: warms the cache
        size = read_file(path)

    times = []
    for _ in range(iterations):
        t0 = time.perf_counter_ns()
        read_file(path)
        times.append(time.perf_counter_ns() - t0)

    print(size)
    print("\n".join(map(str, times)))


if __name__ == "__main__":
    main()
