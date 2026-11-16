import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn

from .data import make_loaders
from .model import DigitsClassifier


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def train_epoch(model, loader, optimizer):
    model.train()
    total_loss = 0.0
    count = 0
    for x, y in loader:
        optimizer.zero_grad()
        loss = nn.functional.cross_entropy(model(x), y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(y)
        count += len(y)
    if count == 0:
        raise ValueError("The training loader is empty")
    return total_loss / count


@torch.no_grad()
def evaluate(model, loader):
    model.eval()
    correct, total = 0, 0
    for x, y in loader:
        correct += int((model(x).argmax(dim=1) == y).sum())
        total += len(y)
    if total == 0:
        raise ValueError("The evaluation loader is empty")
    return correct / total


def train_model(epochs=10, lr=0.01, hidden=32, batch_size=64, seed=42, callback=None):
    if epochs < 1 or lr <= 0:
        raise ValueError("epochs and lr must be positive")
    seed_everything(seed)
    train_loader, test_loader = make_loaders(batch_size=batch_size, seed=seed)
    model = DigitsClassifier(hidden=hidden)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    losses = []
    for epoch in range(epochs):
        loss = train_epoch(model, train_loader, optimizer)
        losses.append(loss)
        if callback is not None:
            callback(epoch, loss)
    # The held-out split is evaluated once, after training.
    score = evaluate(model, test_loader)
    return model, {"train_loss": losses, "test_accuracy": score}


def save_run(model, metrics, output, hidden):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    torch.save(
        {"hidden": hidden, "state_dict": model.state_dict()}, output / "model.pt"
    )
    (output / "metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--hidden", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("hw04/artifacts"))
    args = parser.parse_args()
    model, metrics = train_model(
        epochs=args.epochs, lr=args.lr, hidden=args.hidden, seed=args.seed
    )
    save_run(model, metrics, args.output, args.hidden)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
