from __future__ import annotations


def build_device_summary_text(label: str, summary: dict[str, object]) -> str:
    if not summary["rows"]:
        return f"{label}: no rows matched the selected filters."
    return (
        f"{label} contains {summary['rows']} rows in the selected window. "
        f"Mean device coherence is {summary['mean_coherence']:.2f}, "
        f"with values ranging from {summary['min_coherence']:.2f} to {summary['max_coherence']:.2f}. "
        f"Rows above normal significance: {summary['elevated_rows']}. "
        f"Estimated data coverage is {summary['coverage_pct']:.1f}%."
    )


def build_network_summary_text(label: str, summary: dict[str, object]) -> str:
    if not summary["rows"]:
        return f"{label}: no rows matched the selected filters."
    return (
        f"{label} contains {summary['rows']} rows in the selected window. "
        f"Mean network coherence is {summary['mean_coherence']:.4f}. "
        f"Maximum absolute cumulative coherence is {summary['max_abs_cumsum']:.2f}. "
        f"Average active devices: {summary['active_devices_mean']:.1f}."
    )
