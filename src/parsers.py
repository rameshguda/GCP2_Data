"""
CSV file detection, validation, and normalization.

Handles both Device Coherence and Network Coherence CSV files
downloaded from gcp2.net. Supports .csv and .zip uploads.
"""

from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass, field

import pandas as pd

from src.constants import DEVICE_REQUIRED_COLUMNS, NETWORK_REQUIRED_COLUMNS


@dataclass
class ParsedDataset:
    """Container for a parsed and validated CSV dataset."""

    df: pd.DataFrame
    dataset_type: str                    # "device" or "network"
    device_id: int | None = None         # Only for device files
    group_name: str | None = None        # Only for network files
    filename: str = ""
    row_count: int = 0
    date_min: pd.Timestamp | None = None
    date_max: pd.Timestamp | None = None
    warnings: list[str] = field(default_factory=list)


def detect_dataset_type(df: pd.DataFrame) -> str:
    """Identify whether a DataFrame is device or network coherence data."""
    columns = {col.strip().lower() for col in df.columns}
    normalized_device = {c.lower() for c in DEVICE_REQUIRED_COLUMNS}
    normalized_network = {c.lower() for c in NETWORK_REQUIRED_COLUMNS}

    if normalized_device.issubset(columns):
        return "device"
    elif normalized_network.issubset(columns):
        return "network"
    return "unknown"


def _read_csv_from_bytes(raw: bytes) -> pd.DataFrame:
    """Read CSV from raw bytes, handling common encoding issues."""
    return pd.read_csv(io.BytesIO(raw))


def _extract_csv_from_zip(raw: bytes) -> tuple[bytes, str]:
    """Extract the first CSV file found inside a ZIP archive."""
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise ValueError("ZIP file contains no CSV files")
        name = csv_names[0]
        return zf.read(name), name


def _extract_device_id(df: pd.DataFrame, filename: str) -> int | None:
    """Extract device ID from data column or filename."""
    if "device_number" in df.columns and not df["device_number"].empty:
        return int(df["device_number"].iloc[0])

    match = re.search(r"[Dd]evice[_\s-]?(\d+)", filename)
    if match:
        return int(match.group(1))
    return None


def _extract_group_name(filename: str) -> str:
    """Extract network group name from filename pattern."""
    # e.g. "GCP2_Network_Coherence_Global_Network_2026_03.csv"
    match = re.search(r"Network_Coherence_(.+?)(?:_\d{4}|\.csv)", filename)
    if match:
        return match.group(1).replace("_", " ")
    return "Network"


def _normalize_device_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Normalize and validate a device coherence DataFrame."""
    warnings: list[str] = []

    df["device_number"] = pd.to_numeric(df["device_number"], errors="coerce")
    df["epoch_time_utc"] = pd.to_numeric(df["epoch_time_utc"], errors="coerce")
    df["active_seconds"] = pd.to_numeric(df["active_seconds"], errors="coerce")
    df["device_coherence"] = pd.to_numeric(df["device_coherence"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["epoch_time_utc", "device_coherence"])
    dropped = before - len(df)
    if dropped > 0:
        warnings.append(f"Dropped {dropped} rows with invalid numeric values")

    df["datetime_utc"] = pd.to_datetime(df["epoch_time_utc"], unit="s", utc=True)
    df = df.sort_values("datetime_utc").reset_index(drop=True)

    low_coverage = (df["active_seconds"] < 3600).sum()
    if low_coverage > 0:
        warnings.append(f"{low_coverage} rows have active_seconds < 3600 (partial hours)")

    return df, warnings


def _normalize_network_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Normalize and validate a network coherence DataFrame."""
    warnings: list[str] = []

    df["epoch_time_utc"] = pd.to_numeric(df["epoch_time_utc"], errors="coerce")
    df["network_coherence"] = pd.to_numeric(df["network_coherence"], errors="coerce")
    df["active_devices"] = pd.to_numeric(df["active_devices"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["epoch_time_utc", "network_coherence"])
    dropped = before - len(df)
    if dropped > 0:
        warnings.append(f"Dropped {dropped} rows with invalid numeric values")

    df["datetime_utc"] = pd.to_datetime(df["epoch_time_utc"], unit="s", utc=True)
    df = df.sort_values("datetime_utc").reset_index(drop=True)

    device_range = df["active_devices"].max() - df["active_devices"].min()
    if device_range > 10:
        warnings.append(
            f"Active device count varies by {int(device_range)} "
            f"({int(df['active_devices'].min())} to {int(df['active_devices'].max())})"
        )

    return df, warnings


def _check_time_gaps(df: pd.DataFrame, expected_interval: int) -> list[str]:
    """Detect gaps in the time series."""
    warnings: list[str] = []
    if len(df) < 2:
        return warnings

    diffs = df["epoch_time_utc"].diff().dropna()
    gap_threshold = expected_interval * 3
    gaps = diffs[diffs > gap_threshold]

    if len(gaps) > 0:
        warnings.append(
            f"Detected {len(gaps)} time gaps larger than {gap_threshold}s "
            f"(max gap: {int(gaps.max())}s)"
        )

    dupes = df["epoch_time_utc"].duplicated().sum()
    if dupes > 0:
        warnings.append(f"{dupes} duplicate timestamps found")

    return warnings


def parse_uploaded_file(raw_bytes: bytes, filename: str) -> ParsedDataset:
    """
    Parse an uploaded file (CSV or ZIP) into a validated ParsedDataset.

    This is the main entry point for file ingestion.
    """
    # Extract CSV content
    if filename.lower().endswith(".zip"):
        csv_bytes, inner_name = _extract_csv_from_zip(raw_bytes)
        source_name = inner_name
    else:
        csv_bytes = raw_bytes
        source_name = filename

    # Read and normalize column names
    df = _read_csv_from_bytes(csv_bytes)
    df.columns = [col.strip() for col in df.columns]

    # Detect type
    dataset_type = detect_dataset_type(df)
    if dataset_type == "unknown":
        device_cols = ", ".join(sorted(DEVICE_REQUIRED_COLUMNS))
        network_cols = ", ".join(sorted(NETWORK_REQUIRED_COLUMNS))
        raise ValueError(
            f"Could not identify file type from columns: {list(df.columns)}.\n"
            f"Expected Device columns: {device_cols}\n"
            f"Expected Network columns: {network_cols}"
        )

    # Normalize based on type
    all_warnings: list[str] = []

    if dataset_type == "device":
        df, warnings = _normalize_device_df(df)
        all_warnings.extend(warnings)
        all_warnings.extend(_check_time_gaps(df, expected_interval=60))

        device_id = _extract_device_id(df, source_name)
        return ParsedDataset(
            df=df,
            dataset_type="device",
            device_id=device_id,
            filename=filename,
            row_count=len(df),
            date_min=df["datetime_utc"].min() if len(df) > 0 else None,
            date_max=df["datetime_utc"].max() if len(df) > 0 else None,
            warnings=all_warnings,
        )
    else:
        df, warnings = _normalize_network_df(df)
        all_warnings.extend(warnings)
        all_warnings.extend(_check_time_gaps(df, expected_interval=1))

        group_name = _extract_group_name(source_name)
        return ParsedDataset(
            df=df,
            dataset_type="network",
            group_name=group_name,
            filename=filename,
            row_count=len(df),
            date_min=df["datetime_utc"].min() if len(df) > 0 else None,
            date_max=df["datetime_utc"].max() if len(df) > 0 else None,
            warnings=all_warnings,
        )
