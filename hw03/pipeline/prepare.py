import math

from .common import read_json, read_rows, write_rows


def main():
    min_x = read_json("params.json")["prepare"]["min_x"]
    clean = []
    for row in read_rows("data/raw.csv"):
        try:
            x, target = float(row["x"]), float(row["target"])
        except (ValueError, TypeError):
            continue
        if math.isfinite(x) and math.isfinite(target) and x >= min_x:
            clean.append(row)
    if len(clean) < 10:
        raise ValueError("At least 10 complete observations are required")
    write_rows("data/clean.csv", clean)


if __name__ == "__main__":
    main()
