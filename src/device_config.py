"""
Device naming and configuration system.

Allows users to assign custom names to device IDs (e.g., Device 15 -> "Lab1").
Configuration persists to a JSON file within the session/app directory.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

CONFIG_FILE = Path("device_config.json")


def _load_raw() -> dict:
    """Load the raw config dict from disk."""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"devices": {}, "last_updated": None}


def _save_raw(config: dict) -> None:
    """Write config dict to disk."""
    config["last_updated"] = datetime.now(timezone.utc).isoformat()
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def get_all_devices() -> dict[str, dict]:
    """Return all configured devices as {device_id_str: {name, location, notes}}."""
    return _load_raw().get("devices", {})


def get_device_name(device_id: int) -> str | None:
    """Get the custom name for a device, or None if not configured."""
    devices = get_all_devices()
    entry = devices.get(str(device_id))
    if entry:
        return entry.get("name")
    return None


def get_device_label(device_id: int) -> str:
    """
    Get the display label for a device.

    Returns "{name} (Device {id})" if named, otherwise "Device {id}".
    """
    name = get_device_name(device_id)
    if name:
        return f"{name} (Device {device_id})"
    return f"Device {device_id}"


def set_device_config(
    device_id: int,
    name: str,
    location: str = "",
    notes: str = "",
) -> None:
    """Save or update the configuration for a device."""
    config = _load_raw()
    config["devices"][str(device_id)] = {
        "name": name,
        "location": location,
        "notes": notes,
    }
    _save_raw(config)


def remove_device_config(device_id: int) -> None:
    """Remove configuration for a device."""
    config = _load_raw()
    config["devices"].pop(str(device_id), None)
    _save_raw(config)


def export_config() -> str:
    """Export the full config as a JSON string (for download)."""
    return json.dumps(_load_raw(), indent=2)


def import_config(json_str: str) -> None:
    """Import config from a JSON string (from upload)."""
    config = json.loads(json_str)
    if "devices" not in config:
        raise ValueError("Invalid config: missing 'devices' key")
    _save_raw(config)
