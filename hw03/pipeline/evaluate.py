from math import sqrt
from statistics import mean

from .common import read_json, read_rows, write_json


def main():
    model = read_json("artifacts/model.json")
    rows = read_rows("data/test.csv")
    y = [float(row["target"]) for row in rows]
    pred = [model["slope"] * float(row["x"]) + model["intercept"] for row in rows]
    errors = [a - b for a, b in zip(y, pred)]
    sst = sum((value - mean(y)) ** 2 for value in y)
    metrics = {
        "mae": mean(abs(error) for error in errors),
        "rmse": sqrt(mean(error**2 for error in errors)),
        "r2": 1 - sum(error**2 for error in errors) / sst if sst else 0.0,
    }
    write_json("metrics.json", metrics)
    print(metrics)


if __name__ == "__main__":
    main()
