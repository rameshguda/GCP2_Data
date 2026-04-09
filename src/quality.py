from __future__ import annotations

import pandas as pd


def detect_quality_issues(df: pd.DataFrame, data_type: str) -> list[str]:
    if df.empty:
        return ["No rows matched the selected filters."]

    issues: list[str] = []
    time_deltas = df["datetime_utc"].diff().dropna().dt.total_seconds()

    if data_type == "device":
        if not time_deltas.empty and time_deltas.max() > 60:
            issues.append(
                f"Detected a device data gap of {int(time_deltas.max())} seconds. Some intervals may be missing."
            )
        if "active_seconds" in df.columns:
            low_coverage_rows = int((df["active_seconds"].fillna(0) < 3600).sum())
            if low_coverage_rows:
                issues.append(
                    f"{low_coverage_rows} rows have less than 3600 active seconds, indicating reduced data coverage."
                )
    elif data_type == "network":
        if not time_deltas.empty and time_deltas.max() > 1:
            issues.append(
                f"Detected a network data gap of {int(time_deltas.max())} seconds. The cumulative plot may include missing periods."
            )
        if "active_devices" in df.columns:
            active_min = df["active_devices"].min()
            active_max = df["active_devices"].max()
            if pd.notna(active_min) and pd.notna(active_max) and active_min != active_max:
                issues.append(
                    f"Active device count changes within this selection from {int(active_min)} to {int(active_max)}."
                )

    duplicate_epochs = int(df["epoch_time_utc"].duplicated().sum())
    if duplicate_epochs:
        issues.append(f"Found {duplicate_epochs} duplicate timestamp rows.")

    return issues
