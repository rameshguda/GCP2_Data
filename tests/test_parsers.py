"""Tests for CSV parsing and file detection."""

import pandas as pd
import pytest

from src.parsers import detect_dataset_type, parse_uploaded_file


def _make_device_csv(device_id: int = 337, rows: int = 5) -> bytes:
    """Create a minimal valid device coherence CSV as bytes."""
    lines = ["device_number,epoch_time_utc,active_seconds,device_coherence,significance"]
    base_epoch = 1700000000
    for i in range(rows):
        lines.append(f"{device_id},{base_epoch + i * 60},3600,{50 + i * 10},Normal")
    return "\n".join(lines).encode("utf-8")


def _make_network_csv(rows: int = 5) -> bytes:
    """Create a minimal valid network coherence CSV as bytes."""
    lines = ["epoch_time_utc,network_coherence,active_devices"]
    base_epoch = 1700000000
    for i in range(rows):
        lines.append(f"{base_epoch + i},{0.5 - i * 0.2},350")
    return "\n".join(lines).encode("utf-8")


class TestDetectDatasetType:
    def test_device_detection(self):
        df = pd.read_csv(
            pd.io.common.StringIO(
                "device_number,epoch_time_utc,active_seconds,device_coherence,significance\n"
                "15,1700000000,3600,50.0,Normal"
            )
        )
        assert detect_dataset_type(df) == "device"

    def test_network_detection(self):
        df = pd.read_csv(
            pd.io.common.StringIO(
                "epoch_time_utc,network_coherence,active_devices\n"
                "1700000000,0.5,350"
            )
        )
        assert detect_dataset_type(df) == "network"

    def test_unknown_type(self):
        df = pd.DataFrame({"col_a": [1], "col_b": [2]})
        assert detect_dataset_type(df) == "unknown"

    def test_whitespace_in_columns(self):
        df = pd.read_csv(
            pd.io.common.StringIO(
                " device_number , epoch_time_utc , active_seconds , device_coherence , significance \n"
                "15,1700000000,3600,50.0,Normal"
            )
        )
        # After stripping, should detect as device
        df.columns = [c.strip() for c in df.columns]
        assert detect_dataset_type(df) == "device"


class TestParseUploadedFile:
    def test_parse_device_csv(self):
        raw = _make_device_csv(device_id=15, rows=10)
        result = parse_uploaded_file(raw, "GCP2_Device_Coherence_Device_15_Latest.csv")
        assert result.dataset_type == "device"
        assert result.device_id == 15
        assert result.row_count == 10
        assert "datetime_utc" in result.df.columns

    def test_parse_network_csv(self):
        raw = _make_network_csv(rows=20)
        result = parse_uploaded_file(raw, "GCP2_Network_Coherence_Global_Network_2026_03.csv")
        assert result.dataset_type == "network"
        assert result.group_name == "Global Network"
        assert result.row_count == 20
        assert "datetime_utc" in result.df.columns

    def test_device_id_extracted_from_data(self):
        raw = _make_device_csv(device_id=53)
        result = parse_uploaded_file(raw, "some_random_name.csv")
        assert result.device_id == 53

    def test_invalid_file_raises(self):
        raw = b"col_a,col_b\n1,2\n3,4"
        with pytest.raises(ValueError, match="Could not identify file type"):
            parse_uploaded_file(raw, "bad_file.csv")

    def test_sorted_by_time(self):
        lines = [
            "device_number,epoch_time_utc,active_seconds,device_coherence,significance",
            "15,1700000120,3600,60.0,Normal",
            "15,1700000000,3600,50.0,Normal",
            "15,1700000060,3600,55.0,Normal",
        ]
        raw = "\n".join(lines).encode("utf-8")
        result = parse_uploaded_file(raw, "device.csv")
        epochs = result.df["epoch_time_utc"].tolist()
        assert epochs == sorted(epochs)
