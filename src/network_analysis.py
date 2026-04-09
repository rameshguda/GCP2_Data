from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2


def add_network_metrics(df: pd.DataFrame) -> pd.DataFrame:
    metrics = df.copy()
    metrics["cumulative_coherence"] = metrics["network_coherence"].cumsum()

    n = np.arange(1, len(metrics) + 1)
    # Approximate the 95% confidence envelope described in the GCP2 documentation.
    metrics["envelope_upper"] = np.sqrt(chi2.ppf(0.95, n))
    metrics["envelope_lower"] = -metrics["envelope_upper"]
    return metrics


def network_summary(df: pd.DataFrame) -> dict[str, object]:
    if df.empty:
        return {
            "rows": 0,
            "mean_coherence": None,
            "max_abs_cumsum": None,
            "active_devices_mean": None,
        }

    metrics = add_network_metrics(df)
    return {
        "rows": int(len(metrics)),
        "mean_coherence": float(metrics["network_coherence"].mean()),
        "max_abs_cumsum": float(metrics["cumulative_coherence"].abs().max()),
        "active_devices_mean": float(metrics["active_devices"].mean()),
    }


def network_breakdown(df: pd.DataFrame) -> dict[str, float | int | None]:
    if df.empty:
        return {
            "positive_rows": 0,
            "negative_rows": 0,
            "largest_positive": None,
            "largest_negative": None,
        }

    return {
        "positive_rows": int((df["network_coherence"] > 0).sum()),
        "negative_rows": int((df["network_coherence"] < 0).sum()),
        "largest_positive": float(df["network_coherence"].max()),
        "largest_negative": float(df["network_coherence"].min()),
    }
