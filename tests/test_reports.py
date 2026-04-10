"""Tests for report generation."""

import pandas as pd

from src.device_analysis import device_summary, significance_breakdown
from src.reports import (
    generate_device_report_pdf,
    generate_device_report_text,
    generate_network_report_pdf,
    generate_network_report_text,
)


def _make_device_df():
    base = 1700000000
    return pd.DataFrame({
        "device_number": [337] * 10,
        "epoch_time_utc": [base + i * 60 for i in range(10)],
        "active_seconds": [3600] * 10,
        "device_coherence": [50, 60, 250, 300, 400, 500, 250, 100, 50, 40],
        "significance": [
            "Normal", "Normal", "Elevated", "High", "Very High",
            "Extreme", "Elevated", "Normal", "Normal", "Normal",
        ],
        "datetime_utc": pd.to_datetime(
            [base + i * 60 for i in range(10)], unit="s", utc=True
        ),
    })


class TestDeviceReport:
    def test_text_report_contains_device_label(self):
        df = _make_device_df()
        summary = device_summary(df)
        bd = significance_breakdown(df)
        text = generate_device_report_text("Device 337", summary, bd, [], "2026-04-01 to 2026-04-08")
        assert "Device 337" in text
        assert "DEVICE ACTIVITY REPORT" in text

    def test_text_report_contains_breakdown(self):
        df = _make_device_df()
        summary = device_summary(df)
        bd = significance_breakdown(df)
        text = generate_device_report_text("Test", summary, bd, [])
        assert "Normal" in text
        assert "Extreme" in text

    def test_pdf_report_is_bytes(self):
        df = _make_device_df()
        summary = device_summary(df)
        bd = significance_breakdown(df)
        pdf = generate_device_report_pdf("Device 337", summary, bd, [])
        assert isinstance(pdf, (bytes, bytearray))
        assert len(pdf) > 100
        assert bytes(pdf[:4]) == b"%PDF"


class TestNetworkReport:
    def test_text_report_contains_assessment(self):
        summary = {
            "data_points": 600, "duration_seconds": 600, "duration_minutes": 10.0,
            "mean_coherence": 0.05, "final_cumsum": 30.0, "peak_cumsum": 40.0,
            "peak_cumsum_minute": 8.0, "min_cumsum": -5.0, "min_cumsum_minute": 1.0,
            "max_abs_cumsum": 40.0, "active_devices_mean": 350,
            "active_devices_range": "348-352", "envelope_exit": None,
        }
        text = generate_network_report_text("Global Network", summary, "Not significant.", "Test Event")
        assert "NETWORK COHERENCE ANALYSIS REPORT" in text
        assert "Not significant." in text

    def test_pdf_report_is_valid_pdf(self):
        summary = {
            "data_points": 600, "duration_seconds": 600, "duration_minutes": 10.0,
            "mean_coherence": 0.05, "final_cumsum": 30.0, "peak_cumsum": 40.0,
            "peak_cumsum_minute": 8.0, "min_cumsum": -5.0, "min_cumsum_minute": 1.0,
            "max_abs_cumsum": 40.0, "active_devices_mean": 350,
            "active_devices_range": "348-352", "envelope_exit": None,
        }
        pdf = generate_network_report_pdf("Global Network", summary, "Test assessment.")
        assert isinstance(pdf, (bytes, bytearray))
        assert bytes(pdf[:4]) == b"%PDF"
