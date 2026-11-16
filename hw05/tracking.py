from pathlib import Path

import mlflow
from mlflow.tracking import MlflowClient

BASE = Path(__file__).resolve().parent


def configure_tracking(uri=None, experiment="digits-mlops"):
    mlflow.set_tracking_uri(uri or f"sqlite:///{(BASE / 'mlflow.db').as_posix()}")
    client = MlflowClient()
    if client.get_experiment_by_name(experiment) is None:
        artifact_root = BASE / "mlartifacts"
        artifact_root.mkdir(parents=True, exist_ok=True)
        client.create_experiment(experiment, artifact_location=artifact_root.as_uri())
    mlflow.set_experiment(experiment)
