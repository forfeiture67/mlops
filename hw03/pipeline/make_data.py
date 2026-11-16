"""Recreate the same small CSV without an external download."""

import random

from .common import write_rows


def main():
    rng = random.Random(17)
    rows = []
    for index in range(120):
        x = index / 6
        rows.append(
            {"id": index, "x": x, "target": round(2.5 * x + 7 + rng.gauss(0, 0.8), 6)}
        )
    rows.append({"id": 120, "x": 5, "target": ""})
    write_rows("data/raw.csv", rows)
    print("Created data/raw.csv: 120 observations and one incomplete row")


if __name__ == "__main__":
    main()
