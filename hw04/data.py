import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset


def load_datasets(seed=42):
    """Use the bundled dataset; no internet request is needed."""
    digits = load_digits()
    train_idx, test_idx = train_test_split(
        range(len(digits.target)),
        test_size=0.2,
        random_state=seed,
        stratify=digits.target,
    )
    x = torch.tensor(digits.data / 16.0, dtype=torch.float32)
    y = torch.tensor(digits.target, dtype=torch.long)
    return (
        TensorDataset(x[train_idx], y[train_idx]),
        TensorDataset(x[test_idx], y[test_idx]),
    )


def make_loaders(batch_size=64, seed=42):
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    train, test = load_datasets(seed)
    generator = torch.Generator().manual_seed(seed)
    return (
        DataLoader(train, batch_size=batch_size, shuffle=True, generator=generator),
        DataLoader(test, batch_size=batch_size, shuffle=False),
    )
