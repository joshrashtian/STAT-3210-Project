import random
import subprocess
import sys
from pathlib import Path

import pandas as pd

import parameters


def run(cmd: list[str]) -> str:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def compileList():
    Path("bin").mkdir(exist_ok=True)
    subprocess.run(
        ["gcc", "-O2", "-o", "bin/fs_c", "filesystems/filesystem.c"], check=True
    )
    subprocess.run(
        ["go", "build", "-o", "bin/fs_go", "filesystems/filesystem.go"], check=True
    )


def parse_output(lang: str, output: str) -> tuple[int, list[int]]:
    lines = output.splitlines()
    try:
        size = int(lines[0])
        times_ns = [int(line) for line in lines[1:]]
    except (ValueError, IndexError):
        sys.exit(
            f"error: {lang} printed an unexpected format:\n{output[:200]}\n"
            "expected: <size bytes> on line 1, then one integer ns per line"
        )
    return size, times_ns


def main():
    print("compiling go, c...")
    compileList()

    jobs = [
        (lang, cmd, file)
        for lang, cmd in parameters.COMMANDS.items()
        for file in parameters.FILES
    ]

    print("running functions...")
    rows = []
    for _ in range(parameters.REPEATS):
        random.shuffle(jobs)  # keep run order from biasing any one language

        for lang, cmd, file in jobs:
            path = Path("text_files") / file
            if not path.exists():
                print(f"error: {path} does not exist")
                continue

            output = run(cmd + [str(path), str(parameters.ITERATIONS)])
            size, times_ns = parse_output(lang, output)

            for trial, ns in enumerate(times_ns):
                rows.append(
                    {"language": lang, "size": size, "trial": trial, "time_ns": ns}
                )

    df = pd.DataFrame(rows)
    df["time_us"] = df["time_ns"] / 1e3

    print(df.groupby(["language", "size"])["time_us"].describe().round(2))
    df.to_csv("results.csv", index=False)


if __name__ == "__main__":
    main()
