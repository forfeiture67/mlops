import pytest
import torch
from hypothesis import given, settings
from hypothesis import strategies as st

from hw04.model import DenseBlock, DigitsClassifier


@pytest.mark.unit
def test_block_matches_known_weights():
    block = DenseBlock(2, 2)
    with torch.no_grad():
        block.net[0].weight.copy_(torch.eye(2))
        block.net[0].bias.zero_()
    assert torch.equal(block(torch.tensor([[-2.0, 3.0]])), torch.tensor([[0.0, 3.0]]))


@pytest.mark.unit
def test_model_backward_has_finite_gradients():
    model = DigitsClassifier()
    x = torch.rand(5, 64)
    y = torch.tensor([0, 1, 2, 3, 4])
    loss = torch.nn.functional.cross_entropy(model(x), y)
    loss.backward()
    assert all(
        p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters()
    )
    assert any(p.grad.abs().sum() > 0 for p in model.parameters())


@pytest.mark.property
@settings(max_examples=8, deadline=None)
@given(batch=st.integers(1, 17), hidden=st.integers(1, 48))
def test_model_shape_and_values(batch, hidden):
    logits = DigitsClassifier(hidden)(torch.zeros(batch, 64))
    assert logits.shape == (batch, 10)
    assert torch.isfinite(logits).all()


@pytest.mark.unit
def test_invalid_hidden_is_rejected():
    with pytest.raises(ValueError, match="hidden"):
        DigitsClassifier(0)
