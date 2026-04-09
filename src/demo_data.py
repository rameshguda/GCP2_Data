from __future__ import annotations

from pathlib import Path

from src.parsers import ParsedDataset, parse_uploaded_file


RESOURCE_DIR = Path("resources")
DEMO_FILES = [
    RESOURCE_DIR / "GCP2_Device_Coherence_Device_337_Latest.csv",
    RESOURCE_DIR / "GCP2_Network_Coherence_Global_Network_2026_03.csv.zip",
]


def load_demo_datasets() -> list[ParsedDataset]:
    datasets: list[ParsedDataset] = []
    for path in DEMO_FILES:
        if path.exists():
            datasets.append(parse_uploaded_file(path.read_bytes(), path.name))
    return datasets
