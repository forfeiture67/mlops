import argparse

import lightning as L
import mlflow
import mlflow.pytorch
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split

from hw04.data import load_datasets
from hw04.model import DigitsClassifier
from hw04.train import seed_everything

from .tracking import configure_tracking


class LightningDigits(L.LightningModule):
    def __init__(self, hidden=32, lr=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.model = DigitsClassifier(hidden)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        loss = nn.functional.cross_entropy(self(x), y)
        self.log("train_loss", loss, on_step=False, on_epoch=True, batch_size=len(y))
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        self.log("val_loss", nn.functional.cross_entropy(logits, y), batch_size=len(y))
        self.log(
            "val_accuracy", (logits.argmax(1) == y).float().mean(), batch_size=len(y)
        )

    def test_step(self, batch, batch_idx):
        x, y = batch
        self.log(
            "test_accuracy", (self(x).argmax(1) == y).float().mean(), batch_size=len(y)
        )

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--tracking-uri")
    args = parser.parse_args()
    seed_everything(42)
    configure_tracking(args.tracking_uri, experiment="digits-autolog")
    mlflow.pytorch.autolog(log_models=True, checkpoint=False)
    train, test = load_datasets()
    n_val = round(len(train) * 0.15)
    train, val = random_split(
        train, [len(train) - n_val, n_val], generator=torch.Generator().manual_seed(42)
    )
    train_loader = DataLoader(
        train, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(42)
    )
    val_loader = DataLoader(val, batch_size=64)
    test_loader = DataLoader(test, batch_size=64)
    model = LightningDigits()
    trainer = L.Trainer(
        max_epochs=args.epochs,
        accelerator="cpu",
        devices=1,
        deterministic=True,
        logger=False,
        enable_checkpointing=False,
        enable_progress_bar=False,
        enable_model_summary=False,
    )
    with mlflow.start_run(run_name="lightning-autolog"):
        mlflow.set_tag("homework", "05")
        trainer.fit(model, train_loader, val_loader)
        trainer.test(model, test_loader)


if __name__ == "__main__":
    main()
