import random

from .common import read_json, read_rows, write_rows


def main():
    params = read_json("params.json")["split"]
    if not 0 < params["test_ratio"] < 1:
        raise ValueError("test_ratio must be between 0 and 1")
    rows = read_rows("data/clean.csv")
    random.Random(params["seed"]).shuffle(rows)
    n_test = max(1, round(len(rows) * params["test_ratio"]))
    if len(rows) - n_test < 2:
        raise ValueError("Not enough training observations")
    write_rows("data/train.csv", rows[n_test:])
    write_rows("data/test.csv", rows[:n_test])


if __name__ == "__main__":
    main()
