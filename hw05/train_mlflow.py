import argparse
import json
from importlib.metadata import version
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.pytorch
import torch
from mlflow.models import infer_signature

from hw04.data import make_loaders
from hw04.train import train_model

from .tracking import configure_tracking


def run_experiment(lr=0.01, hidden=32, epochs=10, seed=42, artifacts=False):
    with mlflow.start_run(
        run_name=f"{'artifacts' if artifacts else 'manual'}-lr{lr}-h{hidden}"
    ) as run:
        mlflow.log_params(
            {
                "lr": lr,
                "hidden": hidden,
                "epochs": epochs,
                "seed": seed,
                "batch_size": 64,
            }
        )
        mlflow.set_tags(
            {"homework": "05", "dataset": "sklearn_digits", "logging": "manual"}
        )
        model, metrics = train_model(
            epochs=epochs,
            lr=lr,
            hidden=hidden,
            seed=seed,
            callback=lambda epoch, loss: mlflow.log_metric(
                "train_loss", loss, step=epoch
            ),
        )
        mlflow.log_metric("test_accuracy", metrics["test_accuracy"])
        if artifacts:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(range(1, epochs + 1), metrics["train_loss"], marker=".")
            ax.set(
                xlabel="Epoch", ylabel="Train cross entropy", title="Digits training"
            )
            fig.tight_layout()
            mlflow.log_figure(fig, "loss.png")
            plt.close(fig)
            _, test_loader = make_loaders(seed=seed)
            x, y = next(iter(test_loader))
            with torch.no_grad():
                outputs = model(x[:12]).numpy()
            predictions = outputs.argmax(axis=1)
            fig, axes = plt.subplots(2, 6, figsize=(10, 4))
            for i, ax in enumerate(axes.flat):
                ax.imshow(x[i].reshape(8, 8), cmap="gray_r")
                ax.set_title(
                    f"y={int(y[i])}, p={predictions[i]}",
                    color="green" if predictions[i] == int(y[i]) else "red",
                )
                ax.axis("off")
            fig.tight_layout()
            mlflow.log_figure(fig, "predictions.png")
            plt.close(fig)
            mlflow.log_text(str(model), "model_summary.txt")
            mlflow.log_dict(metrics, "metrics.json")
            mlflow.pytorch.log_model(
                model,
                name="model",
                input_example=x[:12].numpy(),
                signature=infer_signature(x[:12].numpy(), outputs),
                pip_requirements=[
                    f"torch=={version('torch').split('+')[0]}",
                    f"numpy=={version('numpy')}",
                ],
                serialization_format="pickle",
            )
        result = {"run_id": run.info.run_id, "lr": lr, "hidden": hidden, **metrics}
        print(json.dumps(result, indent=2))
        return result


def main(default_artifacts=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracking-uri")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--artifacts", action="store_true", default=default_artifacts)
    parser.add_argument(
        "--output", type=Path, default=Path("hw05/results/manual_runs.json")
    )
    args = parser.parse_args()
    configure_tracking(args.tracking_uri)
    results = [
        run_experiment(
            lr=lr, hidden=hidden, epochs=args.epochs, artifacts=args.artifacts
        )
        for lr, hidden in [(0.01, 32), (0.001, 32), (0.01, 64)]
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
