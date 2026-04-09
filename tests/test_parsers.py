from pathlib import Path

from src.parsers import parse_uploaded_file


RESOURCE_DIR = Path("/Users/heartmath/Documents/GCP2_Data/resources")


def test_parse_device_csv() -> None:
    path = RESOURCE_DIR / "GCP2_Device_Coherence_Device_337_Latest.csv"
    parsed = parse_uploaded_file(path.read_bytes(), path.name)
    assert parsed.data_type == "device"
    assert parsed.device_id == "337"
    assert "datetime_utc" in parsed.dataframe.columns


def test_parse_network_zip() -> None:
    path = RESOURCE_DIR / "GCP2_Network_Coherence_Global_Network_2026_03.csv.zip"
    parsed = parse_uploaded_file(path.read_bytes(), path.name)
    assert parsed.data_type == "network"
    assert parsed.group_name == "Global Network"
    assert "datetime_utc" in parsed.dataframe.columns
