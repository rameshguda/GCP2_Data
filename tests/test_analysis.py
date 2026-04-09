import pandas as pd

from src.device_analysis import significance_breakdown
from src.network_analysis import add_network_metrics, network_breakdown


def test_significance_breakdown_percentages_sum_to_100() -> None:
    df = pd.DataFrame(
        {
            "significance": ["Normal", "High", "Normal", "Extreme"],
            "device_coherence": [1.0, 2.0, 3.0, 4.0],
            "active_seconds": [3600, 3600, 3600, 3600],
            "epoch_time_utc": [1, 2, 3, 4],
            "datetime_utc": pd.to_datetime([1, 2, 3, 4], unit="s", utc=True),
        }
    )
    breakdown = significance_breakdown(df)
    assert round(float(breakdown["percent"].sum()), 6) == 100.0


def test_network_metrics_add_expected_columns() -> None:
    df = pd.DataFrame(
        {
            "epoch_time_utc": [1, 2, 3],
            "network_coherence": [0.5, -0.25, 1.25],
            "active_devices": [100, 101, 102],
            "datetime_utc": pd.to_datetime([1, 2, 3], unit="s", utc=True),
            "datetime_display": pd.to_datetime([1, 2, 3], unit="s", utc=True),
        }
    )
    metrics = add_network_metrics(df)
    assert "cumulative_coherence" in metrics.columns
    assert "envelope_upper" in metrics.columns
    assert "envelope_lower" in metrics.columns
    breakdown = network_breakdown(df)
    assert breakdown["positive_rows"] == 2
    assert breakdown["negative_rows"] == 1
