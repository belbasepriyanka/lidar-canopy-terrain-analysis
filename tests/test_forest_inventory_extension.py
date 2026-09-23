"""Tests for operational forestry analytics extension."""
import numpy as np
import pytest

from src.forest_inventory_extension import (
    canopy_metrics,
    validation_metrics,
    canopy_change,
    build_priority_score,
)


def test_canopy_metrics():
    result = canopy_metrics(np.array([[0, 2, 4], [6, 8, np.nan]]))
    assert result["n_cells"] == 5
    assert result["canopy_cover_pct"] == pytest.approx(80)
    assert result["max_height_m"] == 8


def test_validation_metrics():
    v = validation_metrics([10, 20, 30], [11, 19, 32])
    assert v.n == 3
    assert v.mae_m == pytest.approx(4 / 3)
    assert v.rmse_m == pytest.approx(np.sqrt(2))
    assert v.bias_m == pytest.approx(2 / 3)


def test_change_and_priority():
    t1 = np.array([[1., 3.], [5., 7.]])
    t2 = np.array([[2., 4.], [3., 9.]])
    delta = canopy_change(t1, t2)
    assert delta.shape == (2, 2)
    assert delta[1, 0] == -2
    priority = build_priority_score(delta, t2, np.array([[0.4, 0.5], [0.6, 0.8]]))
    assert np.all((priority >= 0) & (priority <= 100))


def test_shape_mismatch():
    with pytest.raises(ValueError):
        canopy_change(np.zeros((2, 2)), np.zeros((3, 3)))
