"""
Network Coherence analysis engine.

Computes cumulative sums, chi-squared confidence envelopes, and summary metrics
for Network Coherence data downloaded from gcp2.net.

Mathematical reference: GCP2_APP_DEVELOPMENT_PROMPT.md Section 6
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2

from src.constants import CI_95


def add_network_metrics(df: pd.DataFrame, confidence: float = CI_95) -> pd.DataFrame:
    """
    Add computed columns for Event Analysis charting.

    Adds:
      - cumulative_coherence: running cumsum of network_coherence (Red Curve)
      - envelope_upper: upper confidence bound (Blue Envelope, positive)
      - envelope_lower: lower confidence bound (Blue Envelope, negative)

    The envelope is calculated using the chi-squared distribution where
    degrees of freedom at each point equals the number of elapsed seconds
    from the start of the analysis window.
    """
    out = df.copy()

    # Red Curve: cumulative sum of network coherence
    out["cumulative_coherence"] = out["network_coherence"].cumsum()

    # Blue Envelope: 95% CI of chi-squared with increasing df
    # df at second n = n (degrees of freedom equals elapsed seconds)
    n = np.arange(1, len(out) + 1, dtype=np.float64)
    out["envelope_upper"] = np.sqrt(chi2.ppf(confidence, n))
    out["envelope_lower"] = -out["envelope_upper"]

    return out


def network_summary(df: pd.DataFrame) -> dict:
    """
    Compute summary statistics for a network coherence dataset.

    Expects df to already have 'cumulative_coherence' and envelope columns
    (call add_network_metrics first).
    """
    if df.empty:
        return {
            "data_points": 0,
            "duration_seconds": 0,
            "duration_minutes": 0.0,
            "mean_coherence": None,
            "final_cumsum": None,
            "peak_cumsum": None,
            "peak_cumsum_minute": None,
            "min_cumsum": None,
            "min_cumsum_minute": None,
            "max_abs_cumsum": None,
            "active_devices_mean": None,
            "active_devices_range": None,
            "envelope_exit": None,
        }

    n = len(df)
    duration_sec = n  # 1-second granularity
    duration_min = duration_sec / 60.0

    cumsum = df["cumulative_coherence"]
    peak_idx = cumsum.idxmax()
    min_idx = cumsum.idxmin()

    # Determine if/when the red curve exited the envelope
    envelope_exit = _find_envelope_exit(df)

    return {
        "data_points": n,
        "duration_seconds": duration_sec,
        "duration_minutes": round(duration_min, 1),
        "mean_coherence": round(float(df["network_coherence"].mean()), 6),
        "final_cumsum": round(float(cumsum.iloc[-1]), 2),
        "peak_cumsum": round(float(cumsum.max()), 2),
        "peak_cumsum_minute": round((peak_idx + 1) / 60.0, 1) if "minutes" not in df.columns else round(float(df.loc[peak_idx, "minutes"]), 1),
        "min_cumsum": round(float(cumsum.min()), 2),
        "min_cumsum_minute": round((min_idx + 1) / 60.0, 1) if "minutes" not in df.columns else round(float(df.loc[min_idx, "minutes"]), 1),
        "max_abs_cumsum": round(float(cumsum.abs().max()), 2),
        "active_devices_mean": int(df["active_devices"].mean()),
        "active_devices_range": f"{int(df['active_devices'].min())}-{int(df['active_devices'].max())}",
        "envelope_exit": envelope_exit,
    }


def _find_envelope_exit(df: pd.DataFrame) -> dict | None:
    """
    Determine if and when the cumulative sum exits the 95% envelope.

    Returns a dict with exit details, or None if cumsum stays within bounds.
    """
    if "cumulative_coherence" not in df.columns or "envelope_upper" not in df.columns:
        return None

    cumsum = df["cumulative_coherence"]
    upper = df["envelope_upper"]
    lower = df["envelope_lower"]

    # Check upper exit
    above = cumsum > upper
    if above.any():
        first_exit = above.idxmax()
        direction = "upper"
    else:
        # Check lower exit
        below = cumsum < lower
        if below.any():
            first_exit = below.idxmax()
            direction = "lower"
        else:
            return None

    exit_second = first_exit + 1  # 1-indexed
    exit_minute = round(exit_second / 60.0, 1)
    exit_value = round(float(cumsum.iloc[first_exit]), 2)

    return {
        "direction": direction,
        "second": exit_second,
        "minute": exit_minute,
        "cumsum_value": exit_value,
        "significant": True,
    }


def network_breakdown(df: pd.DataFrame) -> dict:
    """Count positive/negative coherence rows and largest values."""
    if df.empty:
        return {
            "positive_rows": 0,
            "negative_rows": 0,
            "zero_rows": 0,
            "largest_positive": None,
            "largest_negative": None,
        }

    nc = df["network_coherence"]
    return {
        "positive_rows": int((nc > 0).sum()),
        "negative_rows": int((nc < 0).sum()),
        "zero_rows": int((nc == 0).sum()),
        "largest_positive": round(float(nc.max()), 4),
        "largest_negative": round(float(nc.min()), 4),
    }


def assess_significance(summary: dict) -> str:
    """
    Generate a plain-language significance assessment from network summary.

    Returns a short paragraph describing whether the data shows
    statistically significant coherence.
    """
    exit_info = summary.get("envelope_exit")

    if exit_info is None:
        final = summary.get("final_cumsum", 0)
        if final is None:
            return "No data available for assessment."

        if abs(final) > 0:
            direction = "upward" if final > 0 else "downward"
            return (
                f"The cumulative sum showed a {direction} trend "
                f"(final value: {final:+.1f}) but remained within the "
                f"95% confidence envelope throughout the analysis window. "
                f"This does not reach statistical significance (p > 0.05)."
            )
        return "The cumulative sum stayed near zero, consistent with random behavior."

    direction_word = "coherence" if exit_info["direction"] == "upper" else "anti-coherence"
    return (
        f"STATISTICALLY SIGNIFICANT: The cumulative sum exited the "
        f"{exit_info['direction']} 95% confidence envelope at minute "
        f"{exit_info['minute']:.1f} (value: {exit_info['cumsum_value']:+.1f}), "
        f"indicating significant network {direction_word} (p < 0.05)."
    )
