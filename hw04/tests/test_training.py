import math

import pytest
import torch
from torch.utils.data import DataLoader, TensorDataset

from hw04.model import DigitsClassifier
from hw04.train import evaluate, seed_everything, train_epoch, train_model


@pytest.mark.integration
def test_epoch_updates_parameters_and_evaluation_bounds():
    seed_everything(3)
    model = DigitsClassifier()
    data = TensorDataset(torch.rand(16, 64), torch.arange(16) % 10)
    loader = DataLoader(data, batch_size=8)
    before = [p.detach().clone() for p in model.parameters()]
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss = train_epoch(model, loader, optimizer)
    assert math.isfinite(loss) and loss > 0
    assert any(not torch.equal(a, b) for a, b in zip(before, model.parameters()))
    assert 0 <= evaluate(model, loader) <= 1


@pytest.mark.training
def test_model_can_overfit_tiny_batch():
    seed_everything(7)
    x = torch.eye(64)[:10]
    y = torch.arange(10)
    loader = DataLoader(TensorDataset(x, y), batch_size=10)
    model = DigitsClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    initial = train_epoch(model, loader, optimizer)
    for _ in range(79):
        final = train_epoch(model, loader, optimizer)
    assert final < initial * 0.1
    assert evaluate(model, loader) == 1.0


@pytest.mark.training
def test_training_reduces_loss_and_is_reproducible():
    first_model, first = train_model(epochs=3, seed=42)
    second_model, second = train_model(epochs=3, seed=42)
    assert first["train_loss"][-1] < first["train_loss"][0]
    assert first["test_accuracy"] > 0.8
    assert first == second
    assert all(
        torch.equal(a, b)
        for a, b in zip(first_model.parameters(), second_model.parameters())
    )


@pytest.mark.integration
def test_evaluation_known_predictions():
    loader = DataLoader(
        TensorDataset(torch.eye(3), torch.tensor([0, 2, 2])), batch_size=2
    )
    assert evaluate(torch.nn.Identity(), loader) == pytest.approx(2 / 3)
