"""
Timezone handling, display conversion, and date/time filtering.

All internal calculations use UTC. Timezone conversion is display-only.
"""

from __future__ import annotations

import pandas as pd


def localize_for_display(df: pd.DataFrame, timezone: str) -> pd.DataFrame:
    """
    Add a 'datetime_display' column converted from UTC to the display timezone.

    The source column 'datetime_utc' must be timezone-aware (UTC).
    """
    out = df.copy()
    out["datetime_display"] = out["datetime_utc"].dt.tz_convert(timezone)
    return out


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: pd.Timestamp | None = None,
    end_date: pd.Timestamp | None = None,
    timezone: str = "UTC",
) -> pd.DataFrame:
    """
    Filter rows by date range using display-timezone dates.

    start_date and end_date should be naive date objects (from a date picker).
    They are interpreted in the given timezone.
    """
    if start_date is None and end_date is None:
        return df

    display_col = "datetime_display" if "datetime_display" in df.columns else "datetime_utc"
    dates = df[display_col].dt.date

    mask = pd.Series(True, index=df.index)
    if start_date is not None:
        mask &= dates >= start_date
    if end_date is not None:
        mask &= dates <= end_date

    return df[mask].reset_index(drop=True)


def filter_by_time_range(
    df: pd.DataFrame,
    start_time=None,
    end_time=None,
) -> pd.DataFrame:
    """
    Filter rows by time-of-day range using display-timezone times.

    Handles wraparound (e.g., 22:00 to 06:00).
    """
    if start_time is None and end_time is None:
        return df

    display_col = "datetime_display" if "datetime_display" in df.columns else "datetime_utc"
    times = df[display_col].dt.time

    mask = pd.Series(True, index=df.index)
    if start_time is not None and end_time is not None:
        if start_time <= end_time:
            mask = (times >= start_time) & (times <= end_time)
        else:
            # Wraparound: e.g., 22:00 to 06:00
            mask = (times >= start_time) | (times <= end_time)
    elif start_time is not None:
        mask = times >= start_time
    elif end_time is not None:
        mask = times <= end_time

    return df[mask].reset_index(drop=True)


def compute_relative_minutes(df: pd.DataFrame, start_epoch: int) -> pd.DataFrame:
    """
    Add a 'minutes' column showing elapsed minutes from a reference epoch.

    Used for Event Analysis charts where x-axis shows relative time.
    """
    out = df.copy()
    out["minutes"] = (out["epoch_time_utc"] - start_epoch) / 60.0
    return out
