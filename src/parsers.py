from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import io
import re
import zipfile

import pandas as pd

DEVICE_REQUIRED_COLUMNS = {
    "device_number",
    "epoch_time_utc",
    "active_seconds",
    "device_coherence",
    "significance",
}

NETWORK_REQUIRED_COLUMNS = {
    "epoch_time_utc",
    "network_coherence",
    "active_devices",
}


@dataclass
class ParsedDataset:
    file_name: str
    data_type: str
    dataframe: pd.DataFrame
    source_label: str
    device_id: str | None = None
    group_name: str | None = None


def _read_csv_from_bytes(raw_bytes: bytes, file_name: str) -> pd.DataFrame:
    if file_name.lower().endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(raw_bytes)) as archive:
            csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
            if not csv_names:
                raise ValueError(f"{file_name} does not contain a CSV file.")
            with archive.open(csv_names[0]) as member:
                return pd.read_csv(member)
    return pd.read_csv(io.BytesIO(raw_bytes))


def detect_dataset_type(df: pd.DataFrame) -> str:
    columns = {column.strip() for column in df.columns}
    if DEVICE_REQUIRED_COLUMNS.issubset(columns):
        return "device"
    if NETWORK_REQUIRED_COLUMNS.issubset(columns):
        return "network"
    raise ValueError(
        "Unsupported CSV schema. Expected device columns "
        f"{sorted(DEVICE_REQUIRED_COLUMNS)} or network columns {sorted(NETWORK_REQUIRED_COLUMNS)}."
    )


def _extract_group_name(file_name: str) -> str | None:
    stem = Path(file_name).stem
    stem = stem.removesuffix(".csv")
    match = re.search(r"Network_Coherence_(.+?)(?:_\d{4}_\d{2})?$", stem, re.IGNORECASE)
    if match:
        return match.group(1).replace("_", " ").strip()
    return None


def parse_uploaded_file(raw_bytes: bytes, file_name: str) -> ParsedDataset:
    df = _read_csv_from_bytes(raw_bytes, file_name)
    df.columns = [column.strip() for column in df.columns]
    dataset_type = detect_dataset_type(df)

    if dataset_type == "device":
        parsed = _normalize_device_df(df)
        device_id = str(parsed["device_number"].iloc[0]) if not parsed.empty else None
        label = f"Device {device_id}" if device_id else file_name
        return ParsedDataset(
            file_name=file_name,
            data_type=dataset_type,
            dataframe=parsed,
            source_label=label,
            device_id=device_id,
        )

    parsed = _normalize_network_df(df)
    group_name = _extract_group_name(file_name) or "Network Group"
    return ParsedDataset(
        file_name=file_name,
        data_type=dataset_type,
        dataframe=parsed,
        source_label=group_name,
        group_name=group_name,
    )


def _normalize_device_df(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized["device_number"] = normalized["device_number"].astype(str)
    normalized["epoch_time_utc"] = pd.to_numeric(normalized["epoch_time_utc"], errors="coerce").astype("Int64")
    normalized["active_seconds"] = pd.to_numeric(normalized["active_seconds"], errors="coerce")
    normalized["device_coherence"] = pd.to_numeric(normalized["device_coherence"], errors="coerce")
    normalized["significance"] = normalized["significance"].astype(str).str.strip()
    normalized = normalized.dropna(subset=["epoch_time_utc", "device_coherence"]).copy()
    normalized["datetime_utc"] = pd.to_datetime(normalized["epoch_time_utc"], unit="s", utc=True)
    return normalized.sort_values("datetime_utc").reset_index(drop=True)


def _normalize_network_df(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized["epoch_time_utc"] = pd.to_numeric(normalized["epoch_time_utc"], errors="coerce").astype("Int64")
    normalized["network_coherence"] = pd.to_numeric(normalized["network_coherence"], errors="coerce")
    normalized["active_devices"] = pd.to_numeric(normalized["active_devices"], errors="coerce")
    normalized = normalized.dropna(subset=["epoch_time_utc", "network_coherence"]).copy()
    normalized["datetime_utc"] = pd.to_datetime(normalized["epoch_time_utc"], unit="s", utc=True)
    return normalized.sort_values("datetime_utc").reset_index(drop=True)
