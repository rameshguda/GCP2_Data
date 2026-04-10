"""Tests for constants and significance classification."""

from src.constants import (
    SIGNIFICANCE_BOUNDARY_VALUES,
    SIGNIFICANCE_ORDER,
    classify_significance,
)


def test_significance_order_has_five_levels():
    assert len(SIGNIFICANCE_ORDER) == 5
    assert SIGNIFICANCE_ORDER[0] == "Normal"
    assert SIGNIFICANCE_ORDER[-1] == "Extreme"


def test_classify_normal():
    assert classify_significance(0) == "Normal"
    assert classify_significance(100) == "Normal"
    assert classify_significance(242) == "Normal"
    assert classify_significance(242.9) == "Normal"


def test_classify_elevated():
    assert classify_significance(243) == "Elevated"
    assert classify_significance(250) == "Elevated"
    assert classify_significance(287) == "Elevated"


def test_classify_high():
    assert classify_significance(288) == "High"
    assert classify_significance(300) == "High"
    assert classify_significance(377) == "High"


def test_classify_very_high():
    assert classify_significance(378) == "Very High"
    assert classify_significance(400) == "Very High"
    assert classify_significance(482) == "Very High"


def test_classify_extreme():
    assert classify_significance(483) == "Extreme"
    assert classify_significance(500) == "Extreme"
    assert classify_significance(1000) == "Extreme"


def test_boundary_values_match_classification():
    """Verify the boundary dict is consistent with classify_significance."""
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["Elevated"]) == "Elevated"
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["High"]) == "High"
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["Very High"]) == "Very High"
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["Extreme"]) == "Extreme"

    # One below each boundary should be the previous level
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["Elevated"] - 1) == "Normal"
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["High"] - 1) == "Elevated"
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["Very High"] - 1) == "High"
    assert classify_significance(SIGNIFICANCE_BOUNDARY_VALUES["Extreme"] - 1) == "Very High"
