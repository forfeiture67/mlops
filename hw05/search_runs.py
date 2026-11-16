import argparse
from pathlib import Path

import mlflow

from .tracking import configure_tracking


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracking-uri")
    parser.add_argument("--experiment", default="digits-mlops")
    parser.add_argument(
        "--output", type=Path, default=Path("hw05/results/experiments.csv")
    )
    args = parser.parse_args()
    configure_tracking(args.tracking_uri, args.experiment)
    runs = mlflow.search_runs(
        experiment_names=[args.experiment], order_by=["metrics.test_accuracy DESC"]
    )
    if runs.empty:
        print("No runs yet. Run python -m hw05.train_artifacts first.")
        return
    columns = [
        c
        for c in [
            "run_id",
            "tags.mlflow.runName",
            "params.lr",
            "params.hidden",
            "metrics.test_accuracy",
            "metrics.train_loss",
        ]
        if c in runs
    ]
    table = runs[columns]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output, index=False)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
