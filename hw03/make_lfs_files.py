"""Two identical small binary files, one for Git and one for Git LFS."""

import argparse
import random
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    output = Path(__file__).resolve().parent / "lfs_demo"
    output.mkdir(exist_ok=True)
    content = random.Random(100 + args.version).randbytes(2 * 1024 * 1024)
    for name in ["plain.bin", "with-lfs.bin"]:
        (output / name).write_bytes(content)
    print(f"Created two identical 2 MiB files, version {args.version}")


if __name__ == "__main__":
    main()
