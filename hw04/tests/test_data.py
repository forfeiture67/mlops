import pytest
import torch

from hw04.data import load_datasets, make_loaders


@pytest.mark.data
def test_dataset_contract_and_disjoint_splits():
    train, test = load_datasets()
    x, y = train.tensors
    assert len(train) + len(test) == 1797
    assert x.dtype == torch.float32 and y.dtype == torch.long
    assert x.shape[1] == 64
    assert torch.isfinite(x).all() and 0 <= x.min() <= x.max() <= 1
    assert set(y.tolist()) == set(range(10))
    # Include labels in keys: exact duplicate observations must not cross the split.
    train_rows = {tuple(row.tolist()) + (int(label),) for row, label in zip(x, y)}
    tx, ty = test.tensors
    test_rows = {tuple(row.tolist()) + (int(label),) for row, label in zip(tx, ty)}
    assert train_rows.isdisjoint(test_rows)


@pytest.mark.data
def test_loader_is_complete_and_reproducible():
    first, _ = make_loaders(batch_size=73, seed=3)
    second, _ = make_loaders(batch_size=73, seed=3)
    batches = list(first)
    assert sum(len(y) for _, y in batches) == len(first.dataset)
    assert len(batches[-1][1]) == len(first.dataset) % 73
    assert torch.equal(batches[0][0], next(iter(second))[0])
    with pytest.raises(ValueError, match="batch_size"):
        make_loaders(batch_size=0)
