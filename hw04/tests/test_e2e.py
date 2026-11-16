import json
import subprocess
import sys
from pathlib import Path

import pytest
import torch

from hw04.data import make_loaders
from hw04.model import DigitsClassifier
from hw04.train import evaluate


@pytest.mark.e2e
def test_cli_trains_saves_and_reloads(tmp_path):
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hw04.train",
            "--epochs",
            "3",
            "--output",
            str(tmp_path),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    metrics = json.loads((tmp_path / "metrics.json").read_text())
    assert metrics["test_accuracy"] > 0.8
    checkpoint = torch.load(tmp_path / "model.pt", weights_only=True)
    model = DigitsClassifier(checkpoint["hidden"])
    model.load_state_dict(checkpoint["state_dict"])
    _, loader = make_loaders()
    assert evaluate(model, loader) == pytest.approx(metrics["test_accuracy"])
