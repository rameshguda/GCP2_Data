"""Tests for network analysis mathematical correctness."""

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2

from src.network_analysis import add_network_metrics, network_summary, _find_envelope_exit


def _make_network_df(seconds: int = 100, coherence_value: float = 0.0) -> pd.DataFrame:
    """Create a test network DataFrame with constant coherence."""
    base = 1700000000
    return pd.DataFrame({
        "epoch_time_utc": range(base, base + seconds),
        "network_coherence": [coherence_value] * seconds,
        "active_devices": [350] * seconds,
        "datetime_utc": pd.to_datetime(
            range(base, base + seconds), unit="s", utc=True
        ),
    })


def _make_trending_network_df(seconds: int = 600, trend: float = 0.1) -> pd.DataFrame:
    """Create a network DataFrame with a consistent positive trend."""
    base = 1700000000
    return pd.DataFrame({
        "epoch_time_utc": range(base, base + seconds),
        "network_coherence": [trend] * seconds,
        "active_devices": [350] * seconds,
        "datetime_utc": pd.to_datetime(
            range(base, base + seconds), unit="s", utc=True
        ),
    })


class TestEnvelopeCalculation:
    def test_envelope_increases_with_time(self):
        """Envelope must widen as degrees of freedom increase (parabolic shape)."""
        df = _make_network_df(seconds=1000)
        result = add_network_metrics(df)
        assert result["envelope_upper"].is_monotonic_increasing

    def test_envelope_is_symmetric(self):
        """Upper and lower envelopes must be exact mirrors."""
        df = _make_network_df(seconds=500)
        result = add_network_metrics(df)
        np.testing.assert_array_almost_equal(
            result["envelope_upper"].values,
            -result["envelope_lower"].values,
        )

    def test_envelope_always_positive_upper(self):
        """Upper envelope must be positive everywhere."""
        df = _make_network_df(seconds=200)
        result = add_network_metrics(df)
        assert (result["envelope_upper"] > 0).all()

    def test_envelope_always_negative_lower(self):
        """Lower envelope must be negative everywhere."""
        df = _make_network_df(seconds=200)
        result = add_network_metrics(df)
        assert (result["envelope_lower"] < 0).all()

    def test_degrees_of_freedom_matches_elapsed_seconds(self):
        """At second N, the envelope must use df=N in chi2.ppf."""
        df = _make_network_df(seconds=100)
        result = add_network_metrics(df)
        n = np.arange(1, 101, dtype=np.float64)
        expected = np.sqrt(chi2.ppf(0.95, n))
        np.testing.assert_array_almost_equal(
            result["envelope_upper"].values, expected
        )

    def test_envelope_at_known_values(self):
        """Verify envelope at specific df values against manual calculation."""
        df = _make_network_df(seconds=3600)
        result = add_network_metrics(df)
        # At df=1: sqrt(chi2.ppf(0.95, 1)) = sqrt(3.8415) = 1.9600
        assert abs(result["envelope_upper"].iloc[0] - 1.96) < 0.01
        # At df=60: sqrt(chi2.ppf(0.95, 60)) = sqrt(79.08) = ~8.893
        assert abs(result["envelope_upper"].iloc[59] - 8.893) < 0.1


class TestCumsum:
    def test_cumsum_of_zeros(self):
        """Cumsum of zero coherence should be all zeros."""
        df = _make_network_df(seconds=100, coherence_value=0.0)
        result = add_network_metrics(df)
        assert (result["cumulative_coherence"] == 0).all()

    def test_cumsum_of_constant_positive(self):
        """Cumsum of constant 1.0 should be 1, 2, 3, ..., N."""
        df = _make_network_df(seconds=50, coherence_value=1.0)
        result = add_network_metrics(df)
        expected = np.arange(1, 51, dtype=np.float64)
        np.testing.assert_array_almost_equal(
            result["cumulative_coherence"].values, expected
        )

    def test_cumsum_of_constant_negative(self):
        """Cumsum of constant -0.5 should trend downward."""
        df = _make_network_df(seconds=100, coherence_value=-0.5)
        result = add_network_metrics(df)
        assert result["cumulative_coherence"].iloc[-1] == pytest.approx(-50.0)

    def test_cumsum_preserves_row_count(self):
        """Output should have same number of rows as input."""
        df = _make_network_df(seconds=500)
        result = add_network_metrics(df)
        assert len(result) == 500


class TestEnvelopeExit:
    def test_no_exit_for_zero_data(self):
        """Zero coherence should never exit the envelope."""
        df = _make_network_df(seconds=1000, coherence_value=0.0)
        result = add_network_metrics(df)
        exit_info = _find_envelope_exit(result)
        assert exit_info is None

    def test_strong_positive_exits_upper(self):
        """A strong positive trend should exit the upper envelope."""
        df = _make_trending_network_df(seconds=600, trend=1.0)
        result = add_network_metrics(df)
        exit_info = _find_envelope_exit(result)
        assert exit_info is not None
        assert exit_info["direction"] == "upper"
        assert exit_info["significant"] is True

    def test_strong_negative_exits_lower(self):
        """A strong negative trend should exit the lower envelope."""
        df = _make_trending_network_df(seconds=600, trend=-1.0)
        result = add_network_metrics(df)
        exit_info = _find_envelope_exit(result)
        assert exit_info is not None
        assert exit_info["direction"] == "lower"


class TestNetworkSummary:
    def test_summary_for_empty_data(self):
        df = pd.DataFrame(columns=["network_coherence", "active_devices", "cumulative_coherence", "envelope_upper", "envelope_lower"])
        result = network_summary(df)
        assert result["data_points"] == 0

    def test_summary_includes_all_keys(self):
        df = _make_network_df(seconds=100)
        df = add_network_metrics(df)
        result = network_summary(df)
        assert "data_points" in result
        assert "final_cumsum" in result
        assert "peak_cumsum" in result
        assert "envelope_exit" in result
        assert "active_devices_mean" in result
