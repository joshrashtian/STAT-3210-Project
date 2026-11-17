COMMANDS: dict[str, list[str]] = {
    "c": ["./bin/fs_c"],
    "go": ["./bin/fs_go"],
    "python": ["python3", "filesystems/filesystem.py"],
}

ITERATIONS: int = 100
REPEATS: int = 5

FILES: list[str] = ["512.txt", "4096.txt", "65536.txt", "1048576.txt", "16777216.txt"]
