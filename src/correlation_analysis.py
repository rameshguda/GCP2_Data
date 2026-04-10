"""
Device-Network Correlation Analysis engine.

Identifies time periods where both Device Coherence and Network Coherence
show simultaneous significance, suggesting local-global alignment.

Device data arrives at ~1-minute intervals; Network at 1-second intervals.
This module handles the time alignment between the two granularities.
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from src.constants import SIGNIFICANCE_ORDER
from src.network_analysis import add_network_metrics


def align_device_network(
    device_df: pd.DataFrame,
    network_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Align device (~1-min) and network (1-sec) data onto a common minute-level
    time axis using the overlapping date range.

    Returns a DataFrame with columns:
      - minute_utc: datetime (UTC), floored to the minute
      - device_coherence: device value for that minute
      - significance: device significance level
      - network_coherence_mean: mean raw network coherence for that minute
      - network_cumsum: cumulative sum of network coherence up to end of minute
      - envelope_upper: envelope value at the end of that minute
    """
    # Find overlapping range
    dev_min = device_df["datetime_utc"].min()
    dev_max = device_df["datetime_utc"].max()
    net_min = network_df["datetime_utc"].min()
    net_max = network_df["datetime_utc"].max()

    overlap_start = max(dev_min, net_min)
    overlap_end = min(dev_max, net_max)

    if overlap_start >= overlap_end:
        return pd.DataFrame()

    # Filter to overlap
    dev = device_df[
        (device_df["datetime_utc"] >= overlap_start)
        & (device_df["datetime_utc"] <= overlap_end)
    ].copy()
    net = network_df[
        (network_df["datetime_utc"] >= overlap_start)
        & (network_df["datetime_utc"] <= overlap_end)
    ].copy()

    if dev.empty or net.empty:
        return pd.DataFrame()

    # Floor device timestamps to minute
    dev["minute_utc"] = dev["datetime_utc"].dt.floor("min")
    dev_agg = dev.groupby("minute_utc").agg(
        device_coherence=("device_coherence", "last"),
        significance=("significance", "last"),
        active_seconds=("active_seconds", "last"),
    ).reset_index()

    # Compute network cumsum over full overlap, then aggregate per minute
    net_metrics = add_network_metrics(net)
    net_metrics["minute_utc"] = net_metrics["datetime_utc"].dt.floor("min")
    net_agg = net_metrics.groupby("minute_utc").agg(
        network_coherence_mean=("network_coherence", "mean"),
        network_cumsum=("cumulative_coherence", "last"),
        envelope_upper=("envelope_upper", "last"),
        envelope_lower=("envelope_lower", "last"),
    ).reset_index()

    # Merge on minute
    merged = pd.merge(dev_agg, net_agg, on="minute_utc", how="inner")
    merged = merged.sort_values("minute_utc").reset_index(drop=True)

    return merged


def find_concurrent_significance(
    aligned_df: pd.DataFrame,
    device_min_level: str = "Elevated",
) -> list[dict]:
    """
    Find time windows where both device and network show simultaneous significance.

    Device significance is compared against the min_level threshold.
    Network significance is determined by whether the cumsum exceeds the envelope.

    Returns a list of dicts describing each concurrent window.
    """
    if aligned_df.empty:
        return []

    rank_map = {label: idx for idx, label in enumerate(SIGNIFICANCE_ORDER)}
    min_rank = rank_map.get(device_min_level, 1)

    df = aligned_df.copy()

    # Device above threshold
    df["device_elevated"] = df["significance"].map(rank_map).fillna(0) >= min_rank

    # Network above envelope (either direction)
    df["network_significant"] = (
        (df["network_cumsum"] > df["envelope_upper"])
        | (df["network_cumsum"] < df["envelope_lower"])
    )

    # Both significant simultaneously
    df["both_significant"] = df["device_elevated"] & df["network_significant"]

    if not df["both_significant"].any():
        return []

    # Group contiguous periods
    df["_group"] = (df["both_significant"] != df["both_significant"].shift()).cumsum()

    periods = []
    for _, group_df in df[df["both_significant"]].groupby("_group"):
        dev_peak_idx = group_df["device_coherence"].idxmax()
        net_peak_idx = group_df["network_cumsum"].abs().idxmax()

        periods.append({
            "start_time": group_df["minute_utc"].iloc[0],
            "end_time": group_df["minute_utc"].iloc[-1],
            "duration_minutes": len(group_df),
            "device_peak": round(float(group_df.loc[dev_peak_idx, "device_coherence"]), 1),
            "device_peak_significance": group_df.loc[dev_peak_idx, "significance"],
            "network_cumsum_peak": round(float(group_df.loc[net_peak_idx, "network_cumsum"]), 2),
            "network_direction": "coherence" if group_df.loc[net_peak_idx, "network_cumsum"] > 0 else "anti-coherence",
        })

    periods.sort(key=lambda p: p["duration_minutes"], reverse=True)
    return periods


def correlation_summary(
    aligned_df: pd.DataFrame,
    concurrent_periods: list[dict],
    device_label: str = "Device",
    network_label: str = "Network",
) -> dict:
    """
    Produce a summary dict for the correlation between device and network data.
    """
    if aligned_df.empty:
        return {
            "overlap_minutes": 0,
            "device_elevated_minutes": 0,
            "network_significant_minutes": 0,
            "concurrent_minutes": 0,
            "concurrent_pct_of_device": 0.0,
            "concurrent_pct_of_network": 0.0,
            "period_count": 0,
            "device_label": device_label,
            "network_label": network_label,
        }

    rank_map = {label: idx for idx, label in enumerate(SIGNIFICANCE_ORDER)}
    device_elevated = (aligned_df["significance"].map(rank_map).fillna(0) >= 1).sum()
    network_sig = (
        (aligned_df["network_cumsum"] > aligned_df["envelope_upper"])
        | (aligned_df["network_cumsum"] < aligned_df["envelope_lower"])
    ).sum()
    concurrent = sum(p["duration_minutes"] for p in concurrent_periods)

    return {
        "overlap_minutes": len(aligned_df),
        "device_elevated_minutes": int(device_elevated),
        "network_significant_minutes": int(network_sig),
        "concurrent_minutes": int(concurrent),
        "concurrent_pct_of_device": round(concurrent / max(device_elevated, 1) * 100, 1),
        "concurrent_pct_of_network": round(concurrent / max(network_sig, 1) * 100, 1),
        "period_count": len(concurrent_periods),
        "device_label": device_label,
        "network_label": network_label,
    }
