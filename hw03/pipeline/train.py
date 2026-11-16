from statistics import mean

from .common import read_rows, write_json


def main():
    rows = read_rows("data/train.csv")
    x = [float(row["x"]) for row in rows]
    y = [float(row["target"]) for row in rows]
    mx, my = mean(x), mean(y)
    denominator = sum((value - mx) ** 2 for value in x)
    if denominator == 0:
        raise ValueError("Feature x must vary")
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / denominator
    write_json("artifacts/model.json", {"slope": slope, "intercept": my - slope * mx})


if __name__ == "__main__":
    main()
