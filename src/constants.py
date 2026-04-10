"""
Single source of truth for all GCP2 Analyzer constants.

Every threshold, color, dimension, and configuration value used across the app
is defined here. No magic numbers should exist elsewhere in the codebase.

Reference: GCP2_APP_DEVELOPMENT_PROMPT.md Section 7 & Appendix A
Source: data_download_calculations.pdf from gcp2.net
"""

# ============================================================
# SIGNIFICANCE THRESHOLDS (from data_download_calculations.pdf)
# Based on simulated distribution of |1-hour moving sum| of chi-squared data
# ============================================================

SIGNIFICANCE_THRESHOLDS = {
    "Normal":    {"min": 0,   "max": 242,  "p_value": "> 0.1"},
    "Elevated":  {"min": 243, "max": 287,  "p_value": "< 0.1"},
    "High":      {"min": 288, "max": 377,  "p_value": "< 0.05"},
    "Very High": {"min": 378, "max": 482,  "p_value": "< 0.01"},
    "Extreme":   {"min": 483, "max": None, "p_value": "< 0.001"},
}

SIGNIFICANCE_ORDER = ["Normal", "Elevated", "High", "Very High", "Extreme"]

SIGNIFICANCE_BOUNDARY_VALUES = {
    "Elevated": 243,
    "High": 288,
    "Very High": 378,
    "Extreme": 483,
}


def classify_significance(value: float) -> str:
    """Classify a smoothed device coherence value into a significance level."""
    if value >= 483:
        return "Extreme"
    elif value >= 378:
        return "Very High"
    elif value >= 288:
        return "High"
    elif value >= 243:
        return "Elevated"
    else:
        return "Normal"


# ============================================================
# EVENT ANALYSIS CHART COLORS (match GCP2.net exactly)
# Red Curve = cumulative sum, Blue Envelope = 95% CI
# ============================================================

EVENT_CHART_COLORS = {
    "red_curve":     "#FF0000",
    "blue_envelope": "#0000FF",
    "zero_baseline": "#000000",
    "event_marker":  "#000000",
    "background":    "#EBEBEB",  # ggplot2 gray -- matches GCP2.net
    "grid":          "#FFFFFF",  # white gridlines on gray background
}

# ============================================================
# DEVICE SIGNIFICANCE COLORS -- Hardware LED Match
# These match the ring of 8 LEDs on the physical NextGen RNG device
# ============================================================

DEVICE_LED_COLORS = {
    "Normal":    "#FF00FF",   # Magenta
    "Elevated":  "#00FFFF",   # Cyan
    "High":      "#FFFF00",   # Yellow
    "Very High": "#FFA500",   # Orange
    "Extreme":   "#FFD700",   # Gold
}

# Muted palette for readability on white backgrounds / print
DEVICE_MUTED_COLORS = {
    "Normal":    "#4F6D7A",   # Steel Blue
    "Elevated":  "#F4A261",   # Sandy Brown
    "High":      "#E76F51",   # Terra Cotta
    "Very High": "#C1121F",   # Crimson
    "Extreme":   "#780000",   # Dark Red
}

# ============================================================
# MULTI-DEVICE COMPARISON PALETTE (colorblind-friendly)
# ============================================================

MULTI_DEVICE_PALETTE = [
    "#1D3557",   # Navy
    "#457B9D",   # Steel Blue
    "#E76F51",   # Burnt Orange
    "#2A9D8F",   # Teal
    "#7B2D8E",   # Amethyst
]

# ============================================================
# CHART DIMENSIONS
# ============================================================

CHART_HEIGHT = 520
CHART_HEIGHT_COMPACT = 420
CHART_EXPORT_WIDTH = 1600
CHART_EXPORT_HEIGHT = 900
CHART_EXPORT_SCALE = 2

# ============================================================
# CHART LINE WIDTHS
# ============================================================

LINE_WIDTH_RED_CURVE = 1.5
LINE_WIDTH_BLUE_ENVELOPE = 1.5
LINE_WIDTH_ZERO_BASELINE = 1.0
LINE_WIDTH_EVENT_MARKER = 2.5
LINE_WIDTH_DEVICE = 2.0
LINE_WIDTH_THRESHOLD = 1.0

# ============================================================
# CONFIDENCE INTERVALS
# ============================================================

CI_95 = 0.95     # Standard Blue Envelope
CI_90 = 0.90     # Near Significant
CI_99 = 0.99     # Very Significant
CI_999 = 0.999   # Extreme

# ============================================================
# DATA CONSTANTS
# ============================================================

DEVICE_INTERVAL_SECONDS = 60
NETWORK_INTERVAL_SECONDS = 1
MAX_ACTIVE_SECONDS = 3600
RNGS_PER_DEVICE = 4
RNGS_USED_FOR_COHERENCE = 3

# ============================================================
# CSV SCHEMA -- required columns for auto-detection
# ============================================================

DEVICE_REQUIRED_COLUMNS = frozenset({
    "device_number",
    "epoch_time_utc",
    "active_seconds",
    "device_coherence",
    "significance",
})

NETWORK_REQUIRED_COLUMNS = frozenset({
    "epoch_time_utc",
    "network_coherence",
    "active_devices",
})

# ============================================================
# TIMEZONE DEFAULTS
# ============================================================

DEFAULT_TIMEZONE = "Asia/Kolkata"

SUPPORTED_TIMEZONES = [
    "UTC",
    "Asia/Kolkata",
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Berlin",
    "Asia/Tokyo",
    "Australia/Sydney",
]

# ============================================================
# UI LIMITS
# ============================================================

MAX_DEVICE_UPLOADS = 5
MAX_COMPARISON_DEVICES = 4
