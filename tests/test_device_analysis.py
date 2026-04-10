"""Tests for device analysis engine."""

import pandas as pd

from src.device_analysis import (
    detect_significant_periods,
    device_summary,
    significance_breakdown,
)


def _make_device_df(rows: int = 20, base_coherence: float = 50.0) -> pd.DataFrame:
    """Create a test device DataFrame with Normal significance."""
    base_epoch = 1700000000
    return pd.DataFrame({
        "device_number": [337] * rows,
        "epoch_time_utc": [base_epoch + i * 60 for i in range(rows)],
        "active_seconds": [3600] * rows,
        "device_coherence": [base_coherence + i for i in range(rows)],
        "significance": ["Normal"] * rows,
        "datetime_utc": pd.to_datetime(
            [base_epoch + i * 60 for i in range(rows)], unit="s", utc=True
        ),
    })


def _make_mixed_significance_df() -> pd.DataFrame:
    """Create a device DataFrame with various significance levels."""
    base_epoch = 1700000000
    data = {
        "device_number": [15] * 10,
        "epoch_time_utc": [base_epoch + i * 60 for i in range(10)],
        "active_seconds": [3600] * 10,
        "device_coherence": [50, 60, 250, 300, 400, 500, 250, 100, 50, 40],
        "significance": [
            "Normal", "Normal", "Elevated", "High", "Very High",
            "Extreme", "Elevated", "Normal", "Normal", "Normal",
        ],
        "datetime_utc": pd.to_datetime(
            [base_epoch + i * 60 for i in range(10)], unit="s", utc=True
        ),
    }
    return pd.DataFrame(data)


class TestDeviceSummary:
    def test_basic_summary(self):
        df = _make_device_df(rows=100)
        result = device_summary(df)
        assert result["rows"] == 100
        assert result["mean_coherence"] is not None
        assert result["max_coherence"] is not None
        assert result["coverage_pct"] == 100.0

    def test_empty_summary(self):
        df = pd.DataFrame(columns=["device_number", "epoch_time_utc", "active_seconds", "device_coherence", "significance", "datetime_utc"])
        result = device_summary(df)
        assert result["rows"] == 0
        assert result["mean_coherence"] is None

    def test_elevated_count(self):
        df = _make_mixed_significance_df()
        result = device_summary(df)
        # Elevated + High + Very High + Extreme = 2 + 1 + 1 + 1 = 5
        assert result["elevated_rows"] == 5

    def test_partial_coverage(self):
        df = _make_device_df(rows=10)
        df["active_seconds"] = 1800  # Half coverage
        result = device_summary(df)
        assert result["coverage_pct"] == 50.0


class TestSignificanceBreakdown:
    def test_breakdown_sums_to_total(self):
        df = _make_mixed_significance_df()
        result = significance_breakdown(df)
        assert result["rows"].sum() == len(df)

    def test_breakdown_percentages(self):
        df = _make_mixed_significance_df()
        result = significance_breakdown(df)
        assert abs(result["percent"].sum() - 100.0) < 0.1

    def test_breakdown_has_p_values(self):
        df = _make_mixed_significance_df()
        result = significance_breakdown(df)
        assert "p_value" in result.columns
        assert "p > 0.1" in result["p_value"].values

    def test_empty_breakdown(self):
        df = pd.DataFrame(columns=["significance"])
        result = significance_breakdown(df)
        assert len(result) == 0


class TestSignificantPeriods:
    def test_no_periods_when_all_normal(self):
        df = _make_device_df(rows=50)
        result = detect_significant_periods(df)
        assert result == []

    def test_detects_elevated_periods(self):
        df = _make_mixed_significance_df()
        result = detect_significant_periods(df, min_level="Elevated")
        assert len(result) >= 1
        # The big period (rows 2-6) should have peak at Extreme (500)
        assert any(p["peak_significance"] == "Extreme" for p in result)

    def test_period_has_required_fields(self):
        df = _make_mixed_significance_df()
        result = detect_significant_periods(df)
        if result:
            p = result[0]
            assert "start_time" in p
            assert "end_time" in p
            assert "duration_minutes" in p
            assert "peak_value" in p
            assert "peak_significance" in p

    def test_periods_sorted_by_peak_descending(self):
        df = _make_mixed_significance_df()
        result = detect_significant_periods(df)
        if len(result) >= 2:
            assert result[0]["peak_value"] >= result[1]["peak_value"]
