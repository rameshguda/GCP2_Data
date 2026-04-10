"""
Device Coherence analysis engine.

Computes summary metrics, significance breakdowns, and detects
significant time periods for Device Coherence data from gcp2.net.

Mathematical reference: GCP2_APP_DEVELOPMENT_PROMPT.md Section 6
"""

from __future__ import annotations

import pandas as pd

from src.constants import (
    MAX_ACTIVE_SECONDS,
    SIGNIFICANCE_BOUNDARY_VALUES,
    SIGNIFICANCE_ORDER,
)


def device_summary(df: pd.DataFrame) -> dict:
    """
    Compute summary statistics for a device coherence dataset.

    Returns a dict with key metrics suitable for display.
    """
    if df.empty:
        return {
            "rows": 0,
            "mean_coherence": None,
            "max_coherence": None,
            "max_significance": None,
            "min_coherence": None,
            "elevated_rows": 0,
            "coverage_pct": None,
            "date_range": None,
        }

    elevated = df["significance"].isin(SIGNIFICANCE_ORDER[1:]).sum()
    coverage = (
        df["active_seconds"].fillna(0) / MAX_ACTIVE_SECONDS
    ).clip(lower=0, upper=1).mean() * 100

    max_idx = df["device_coherence"].idxmax()
    max_sig = df.loc[max_idx, "significance"]

    return {
        "rows": int(len(df)),
        "mean_coherence": round(float(df["device_coherence"].mean()), 1),
        "max_coherence": round(float(df["device_coherence"].max()), 1),
        "max_significance": max_sig,
        "min_coherence": round(float(df["device_coherence"].min()), 1),
        "elevated_rows": int(elevated),
        "coverage_pct": round(float(coverage), 1),
        "date_range": f"{df['datetime_utc'].min()} to {df['datetime_utc'].max()}",
    }


def significance_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tabular breakdown of significance levels with counts and percentages.

    Returns a DataFrame with columns: significance, rows, percent, p_value
    """
    if df.empty:
        return pd.DataFrame(columns=["significance", "rows", "percent", "p_value"])

    p_values = {
        "Normal": "p > 0.1",
        "Elevated": "p < 0.1",
        "High": "p < 0.05",
        "Very High": "p < 0.01",
        "Extreme": "p < 0.001",
    }

    counts = (
        df["significance"]
        .value_counts(dropna=False)
        .rename_axis("significance")
        .reset_index(name="rows")
    )
    counts["percent"] = round(counts["rows"] / len(df) * 100, 1)
    counts["p_value"] = counts["significance"].map(p_values).fillna("")

    # Sort by significance order
    order_map = {label: idx for idx, label in enumerate(SIGNIFICANCE_ORDER)}
    counts["sort_key"] = counts["significance"].map(order_map).fillna(len(SIGNIFICANCE_ORDER))
    counts = counts.sort_values("sort_key").drop(columns=["sort_key"]).reset_index(drop=True)

    return counts


def detect_significant_periods(
    df: pd.DataFrame,
    min_level: str = "Elevated",
) -> list[dict]:
    """
    Identify contiguous time periods where the device reached the specified
    significance level or higher.

    Returns a list of dicts, each describing one significant period with:
      - start_time, end_time
      - duration_minutes
      - peak_value, peak_time, peak_significance
      - mean_active_seconds
    """
    if df.empty:
        return []

    rank_map = {label: idx for idx, label in enumerate(SIGNIFICANCE_ORDER)}
    min_rank = rank_map.get(min_level, 1)

    df = df.copy()
    df["_above"] = df["significance"].map(rank_map).fillna(0) >= min_rank

    if not df["_above"].any():
        return []

    # Identify contiguous groups of above-threshold rows
    df["_group"] = (df["_above"] != df["_above"].shift()).cumsum()

    periods = []
    for _, group_df in df[df["_above"]].groupby("_group"):
        peak_idx = group_df["device_coherence"].idxmax()

        display_col = "datetime_display" if "datetime_display" in group_df.columns else "datetime_utc"

        periods.append({
            "start_time": group_df[display_col].iloc[0],
            "end_time": group_df[display_col].iloc[-1],
            "duration_minutes": len(group_df),  # ~1 row per minute
            "peak_value": round(float(group_df.loc[peak_idx, "device_coherence"]), 1),
            "peak_time": group_df.loc[peak_idx, display_col],
            "peak_significance": group_df.loc[peak_idx, "significance"],
            "mean_active_seconds": round(float(group_df["active_seconds"].mean()), 0),
            "row_count": len(group_df),
        })

    # Sort by peak value descending
    periods.sort(key=lambda p: p["peak_value"], reverse=True)
    return periods


def format_significant_periods(periods: list[dict], max_display: int = 10) -> str:
    """Format significant periods into a readable text block."""
    if not periods:
        return "No periods of elevated significance detected in this time range."

    lines = []
    shown = min(len(periods), max_display)
    for i, p in enumerate(periods[:shown], 1):
        lines.append(
            f"  {i}. {p['start_time']} to {p['end_time']}\n"
            f"     Peak: {p['peak_value']} ({p['peak_significance']}) at {p['peak_time']}\n"
            f"     Duration: {p['duration_minutes']} minutes, "
            f"Active seconds: {p['mean_active_seconds']:.0f}"
        )

    header = f"Top {shown} significant periods (of {len(periods)} total):"
    return header + "\n\n" + "\n\n".join(lines)
