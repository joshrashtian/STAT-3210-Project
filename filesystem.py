import time
from pathlib import Path
import sys

file_path = Path(sys.argv[1]) 
iterate: int = int(sys.argv[2])

start = time.perf_counter_ns()

total: int = 0

for i in range(iterate):
    with open(file_path, "rb") as f:
        while chunk := f.read(512):
            total += len(chunk)

elapsed = time.perf_counter_ns() - start
print(elapsed)
print(total)
