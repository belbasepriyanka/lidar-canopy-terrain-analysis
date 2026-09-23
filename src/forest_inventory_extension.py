"""Forest inventory analytics for LiDAR/UAV remote-sensing workflows.

The functions are intentionally lightweight so they can be reused with
CHM rasters or arrays derived from airborne LiDAR, UAV photogrammetry,
or other canopy-height products.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

import numpy as np


@dataclass(frozen=True)
class ValidationSummary:
    n: int
    mae_m: float
    rmse_m: float
    bias_m: float
    r2: float


def _clean(values: np.ndarray) -> np.ndarray:
    """Return finite floating-point values only."""
    arr = np.asarray(values, dtype=float)
    return arr[np.isfinite(arr)]


def canopy_metrics(
    chm: np.ndarray,
    canopy_threshold_m: float = 2.0,
    max_plausible_height_m: float = 80.0,
) -> Dict[str, float]:
    """Summarize a canopy-height model.

    Parameters
    ----------
    chm:
        Canopy height values in meters.
    canopy_threshold_m:
        Minimum height used to define canopy cover.
    max_plausible_height_m:
        Upper bound used for basic QA/QC.

    Returns
    -------
    dict
        Structural metrics useful for inventory summaries.
    """
    arr = _clean(chm)
    arr = arr[(arr >= 0.0) & (arr <= max_plausible_height_m)]
    if arr.size == 0:
        raise ValueError("No valid canopy-height values remain after QA/QC.")

    canopy = arr >= canopy_threshold_m
    return {
        "n_cells": int(arr.size),
        "mean_height_m": float(np.mean(arr)),
        "median_height_m": float(np.median(arr)),
        "p90_height_m": float(np.percentile(arr, 90)),
        "p95_height_m": float(np.percentile(arr, 95)),
        "max_height_m": float(np.max(arr)),
        "canopy_cover_pct": float(np.mean(canopy) * 100.0),
    }


def validation_metrics(
    observed_height_m: Iterable[float],
    predicted_height_m: Iterable[float],
) -> ValidationSummary:
    """Compare LiDAR/UAV predictions with independent field observations."""
    obs = np.asarray(list(observed_height_m), dtype=float)
    pred = np.asarray(list(predicted_height_m), dtype=float)

    if obs.shape != pred.shape:
        raise ValueError("Observed and predicted arrays must have equal shape.")

    mask = np.isfinite(obs) & np.isfinite(pred)
    obs, pred = obs[mask], pred[mask]

    if obs.size < 2:
        raise ValueError("At least two paired observations are required.")

    residual = pred - obs
    mae = float(np.mean(np.abs(residual)))
    rmse = float(np.sqrt(np.mean(residual**2)))
    bias = float(np.mean(residual))

    ss_res = float(np.sum((obs - pred) ** 2))
    ss_tot = float(np.sum((obs - np.mean(obs)) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")

    return ValidationSummary(
        n=int(obs.size),
        mae_m=mae,
        rmse_m=rmse,
        bias_m=bias,
        r2=r2,
    )


def canopy_change(
    chm_t1: np.ndarray,
    chm_t2: np.ndarray,
    clip_m: float = 20.0,
) -> np.ndarray:
    """Calculate repeat-acquisition canopy-height change with QA clipping."""
    a = np.asarray(chm_t1, dtype=float)
    b = np.asarray(chm_t2, dtype=float)
    if a.shape != b.shape:
        raise ValueError("Input CHMs must have the same shape.")

    change = b - a
    change[~np.isfinite(change)] = np.nan
    return np.clip(change, -clip_m, clip_m)


def build_priority_score(
    canopy_change_m: np.ndarray,
    canopy_height_m: np.ndarray,
    ndvi: np.ndarray,
) -> np.ndarray:
    """Create an illustrative 0-100 scouting-priority score.

    This is a decision-support index, not a calibrated forestry risk model.
    Higher values indicate combinations of larger canopy change, taller
    vegetation, and lower vegetation vigor that may warrant field review.
    """
    change = np.asarray(canopy_change_m, dtype=float)
    height = np.asarray(canopy_height_m, dtype=float)
    vigor = np.asarray(ndvi, dtype=float)

    if not (change.shape == height.shape == vigor.shape):
        raise ValueError("All arrays must have the same shape.")

    def scale01(x: np.ndarray) -> np.ndarray:
        out = np.full_like(x, np.nan, dtype=float)
        valid = np.isfinite(x)
        if not np.any(valid):
            return out
        lo, hi = np.nanpercentile(x[valid], [5, 95])
        if hi <= lo:
            out[valid] = 0.0
            return out
        out[valid] = np.clip((x[valid] - lo) / (hi - lo), 0.0, 1.0)
        return out

    change_component = scale01(np.abs(change))
    height_component = scale01(height)
    low_vigor_component = 1.0 - scale01(vigor)

    score = 100.0 * (
        0.45 * change_component
        + 0.35 * height_component
        + 0.20 * low_vigor_component
    )
    return np.clip(score, 0.0, 100.0)
