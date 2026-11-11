import pandas
import subprocess
import parameters


def run(cmd: list[str]) -> str:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def compileList():
    subprocess.run(
        ["gcc", "-O2", "-o", "bin/fs_c", "filesystems/filesystem.c"], check=True
    )
    subprocess.run(
        ["go", "build", "-o", "bin/fs_go", "filesystems/filesystem.go"], check=True
    )


def main():
    print("compiling go, c...")
    compileList()

    print("running functions...")

    for lang, cmd in parameters.COMMANDS.items():
        for file in parameters.FILES:
            output = run(cmd + [f"text_files/{file}", str(parameters.ITERATIONS)])
        print(lang, file, output)


if __name__ == "__main__":
    main()
