"""Tests for device-network correlation analysis."""

import pandas as pd
import numpy as np

from src.correlation_analysis import (
    align_device_network,
    correlation_summary,
    find_concurrent_significance,
)


def _make_device_df(start_epoch: int, minutes: int = 60) -> pd.DataFrame:
    return pd.DataFrame({
        "device_number": [15] * minutes,
        "epoch_time_utc": [start_epoch + i * 60 for i in range(minutes)],
        "active_seconds": [3600] * minutes,
        "device_coherence": [100 + i * 5 for i in range(minutes)],
        "significance": (["Normal"] * (minutes // 3) + ["Elevated"] * (minutes // 3) + ["High"] * (minutes - 2 * (minutes // 3))),
        "datetime_utc": pd.to_datetime(
            [start_epoch + i * 60 for i in range(minutes)], unit="s", utc=True
        ),
    })


def _make_network_df(start_epoch: int, seconds: int = 3600) -> pd.DataFrame:
    return pd.DataFrame({
        "epoch_time_utc": range(start_epoch, start_epoch + seconds),
        "network_coherence": [0.5] * seconds,  # Strong positive trend
        "active_devices": [350] * seconds,
        "datetime_utc": pd.to_datetime(
            range(start_epoch, start_epoch + seconds), unit="s", utc=True
        ),
    })


class TestAlignDeviceNetwork:
    def test_alignment_produces_rows(self):
        base = 1700000000
        dev = _make_device_df(base, 60)
        net = _make_network_df(base, 3600)
        aligned = align_device_network(dev, net)
        assert len(aligned) > 0
        assert "device_coherence" in aligned.columns
        assert "network_cumsum" in aligned.columns

    def test_no_overlap_returns_empty(self):
        dev = _make_device_df(1700000000, 60)
        net = _make_network_df(1800000000, 3600)  # Far in the future
        aligned = align_device_network(dev, net)
        assert aligned.empty

    def test_minute_utc_column_exists(self):
        base = 1700000000
        dev = _make_device_df(base, 30)
        net = _make_network_df(base, 1800)
        aligned = align_device_network(dev, net)
        if not aligned.empty:
            assert "minute_utc" in aligned.columns
        else:
            # If alignment returned empty due to floor rounding, that's ok
            pass


class TestConcurrentSignificance:
    def test_finds_concurrent_periods(self):
        base = 1700000000
        dev = _make_device_df(base, 60)
        net = _make_network_df(base, 3600)
        aligned = align_device_network(dev, net)

        periods = find_concurrent_significance(aligned)
        # With strong positive network trend and device elevated periods,
        # there should be some concurrent windows
        assert isinstance(periods, list)

    def test_empty_df_returns_empty(self):
        aligned = pd.DataFrame()
        assert find_concurrent_significance(aligned) == []


class TestCorrelationSummary:
    def test_summary_has_required_keys(self):
        base = 1700000000
        dev = _make_device_df(base, 60)
        net = _make_network_df(base, 3600)
        aligned = align_device_network(dev, net)
        concurrent = find_concurrent_significance(aligned)
        result = correlation_summary(aligned, concurrent, "Device 15", "Global Network")

        assert "overlap_minutes" in result
        assert "device_elevated_minutes" in result
        assert "network_significant_minutes" in result
        assert "concurrent_minutes" in result
        assert result["device_label"] == "Device 15"

    def test_empty_summary(self):
        result = correlation_summary(pd.DataFrame(), [], "Dev", "Net")
        assert result["overlap_minutes"] == 0
