COMMANDS: dict[str, list[str]] = {
    "c": ["./bin/fs_c"],
    "go": ["./bin/fs_go"],
    "python": ["python3", "filesystems/filesystem.py"],
}

ITERATIONS: int = 100

FILES: list[str] = ["512.txt", "4096.txt"]
