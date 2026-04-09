from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path


def save_analysis_record(base_dir: Path, payload: dict) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    target = base_dir / f"analysis_{timestamp}.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target
