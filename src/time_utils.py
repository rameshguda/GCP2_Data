from __future__ import annotations

from datetime import date, time
from zoneinfo import ZoneInfo

import pandas as pd


def localize_for_display(df: pd.DataFrame, timezone_name: str) -> pd.DataFrame:
    localized = df.copy()
    tz = ZoneInfo(timezone_name)
    localized["datetime_display"] = localized["datetime_utc"].dt.tz_convert(tz)
    return localized


def filter_by_date_and_time(
    df: pd.DataFrame,
    timezone_name: str,
    start_date: date,
    end_date: date,
    start_time: time,
    end_time: time,
) -> pd.DataFrame:
    localized = localize_for_display(df, timezone_name)
    mask = localized["datetime_display"].dt.date.between(start_date, end_date)

    display_time = localized["datetime_display"].dt.time
    if start_time <= end_time:
        time_mask = display_time.between(start_time, end_time)
    else:
        time_mask = (display_time >= start_time) | (display_time <= end_time)

    return localized[mask & time_mask].copy()
