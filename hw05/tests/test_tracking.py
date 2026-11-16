import numpy as np
import pytest
import torch

from hw05.train_mlflow import run_experiment


@pytest.mark.tracking
def test_logged_model_reload_matches_predictions(tmp_path):
    import mlflow
    import mlflow.pytorch
    from mlflow.tracking import MlflowClient

    mlflow.set_tracking_uri(f"sqlite:///{(tmp_path / 'runs.db').as_posix()}")
    experiment = mlflow.create_experiment(
        "isolated-test", artifact_location=(tmp_path / "artifacts").as_uri()
    )
    mlflow.set_experiment(experiment_id=experiment)
    result = run_experiment(epochs=2, artifacts=True)
    client = MlflowClient()
    run = client.get_run(result["run_id"])
    assert run.info.status == "FINISHED"
    assert run.data.params["epochs"] == "2"
    assert run.data.metrics["test_accuracy"] > 0.7
    assert len(client.get_metric_history(result["run_id"], "train_loss")) == 2
    assert {"loss.png", "predictions.png", "metrics.json", "model_summary.txt"} <= {
        item.path for item in client.list_artifacts(result["run_id"])
    }
    models = mlflow.search_logged_models(
        experiment_ids=[experiment], output_format="list"
    )
    assert len(models) == 1
    native = mlflow.pytorch.load_model(models[0].model_uri)
    pyfunc = mlflow.pyfunc.load_model(models[0].model_uri)
    inputs = np.zeros((3, 64), dtype=np.float32)
    with torch.no_grad():
        expected = native(torch.from_numpy(inputs)).numpy()
    np.testing.assert_allclose(pyfunc.predict(inputs), expected, rtol=1e-5, atol=1e-6)
