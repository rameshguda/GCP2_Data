from __future__ import annotations

import pandas as pd

SIGNIFICANCE_ORDER = ["Normal", "Elevated", "High", "Very High", "Extreme"]
SIGNIFICANCE_COLORS = {
    "Normal": "#4F6D7A",
    "Elevated": "#F4A261",
    "High": "#E76F51",
    "Very High": "#C1121F",
    "Extreme": "#780000",
}


def device_summary(df: pd.DataFrame) -> dict[str, object]:
    if df.empty:
        return {
            "rows": 0,
            "mean_coherence": None,
            "max_coherence": None,
            "min_coherence": None,
            "elevated_rows": 0,
            "coverage_pct": None,
        }

    elevated = df["significance"].isin(SIGNIFICANCE_ORDER[1:]).sum()
    coverage_pct = (df["active_seconds"].fillna(0) / 3600.0).clip(lower=0, upper=1).mean() * 100
    return {
        "rows": int(len(df)),
        "mean_coherence": float(df["device_coherence"].mean()),
        "max_coherence": float(df["device_coherence"].max()),
        "min_coherence": float(df["device_coherence"].min()),
        "elevated_rows": int(elevated),
        "coverage_pct": float(coverage_pct),
    }


def significance_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["significance", "rows", "percent"])

    counts = (
        df["significance"]
        .value_counts(dropna=False)
        .rename_axis("significance")
        .reset_index(name="rows")
    )
    counts["percent"] = counts["rows"] / len(df) * 100
    counts["sort_key"] = counts["significance"].map(
        {label: idx for idx, label in enumerate(SIGNIFICANCE_ORDER)}
    ).fillna(len(SIGNIFICANCE_ORDER))
    counts = counts.sort_values(["sort_key", "significance"]).drop(columns=["sort_key"])
    return counts.reset_index(drop=True)
