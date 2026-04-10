"""
Chart generation for GCP2 Consciousness Data Analyzer.

All charts are built with Plotly and follow the specifications in
GCP2_APP_DEVELOPMENT_PROMPT.md Section 7 (Single Source of Truth).

CRITICAL: The Event Analysis chart must match GCP2.net exactly.
Color codes, axis labels, and visual components are defined in constants.py.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.constants import (
    CHART_HEIGHT,
    CHART_HEIGHT_COMPACT,
    DEVICE_LED_COLORS,
    DEVICE_MUTED_COLORS,
    EVENT_CHART_COLORS,
    LINE_WIDTH_BLUE_ENVELOPE,
    LINE_WIDTH_DEVICE,
    LINE_WIDTH_EVENT_MARKER,
    LINE_WIDTH_RED_CURVE,
    LINE_WIDTH_THRESHOLD,
    LINE_WIDTH_ZERO_BASELINE,
    MULTI_DEVICE_PALETTE,
    SIGNIFICANCE_BOUNDARY_VALUES,
    SIGNIFICANCE_ORDER,
)


# ── Network Coherence Charts ────────────────────────────────


def network_event_analysis_chart(
    df: pd.DataFrame,
    event_title: str = "Event Analysis",
    start_time_display: str = "",
    timezone_label: str = "",
) -> go.Figure:
    """
    Generate the flagship GCP2.net-style Event Analysis chart.

    This is the most important chart in the app. It must match
    GCP2.net exactly: Red Curve (cumsum) + Blue Envelope (95% CI)
    on a relative time axis (minutes from event start).

    Required columns in df:
      - minutes: float, relative time from event start
      - cumulative_coherence: float, running cumsum
      - envelope_upper: float, upper 95% CI
      - envelope_lower: float, lower 95% CI
    """
    colors = EVENT_CHART_COLORS
    fig = go.Figure()

    # 1. Red Curve -- Cumulative Coherence (the primary signal)
    fig.add_trace(go.Scatter(
        x=df["minutes"],
        y=df["cumulative_coherence"],
        mode="lines",
        name="Cumulative Coherence",
        line=dict(color=colors["red_curve"], width=LINE_WIDTH_RED_CURVE),
        hovertemplate="Min: %{x:.1f}<br>Coherence: %{y:.2f}<extra></extra>",
    ))

    # 2. Blue Envelope -- Upper Bound (95% confidence)
    fig.add_trace(go.Scatter(
        x=df["minutes"],
        y=df["envelope_upper"],
        mode="lines",
        name="Envelope (95% CI)",
        line=dict(color=colors["blue_envelope"], width=LINE_WIDTH_BLUE_ENVELOPE),
        hovertemplate="Min: %{x:.1f}<br>Upper: %{y:.2f}<extra></extra>",
    ))

    # 3. Blue Envelope -- Lower Bound (mirror)
    fig.add_trace(go.Scatter(
        x=df["minutes"],
        y=df["envelope_lower"],
        mode="lines",
        name="Envelope (95% CI)",
        line=dict(color=colors["blue_envelope"], width=LINE_WIDTH_BLUE_ENVELOPE),
        showlegend=False,
        hovertemplate="Min: %{x:.1f}<br>Lower: %{y:.2f}<extra></extra>",
    ))

    # 4. Zero Baseline -- horizontal black line at y=0
    fig.add_hline(
        y=0,
        line_color=colors["zero_baseline"],
        line_width=LINE_WIDTH_ZERO_BASELINE,
    )

    # 5. Vertical Event Marker at x=0 (event start)
    fig.add_vline(
        x=0,
        line_color=colors["event_marker"],
        line_width=LINE_WIDTH_EVENT_MARKER,
    )

    # 6. Layout -- match GCP2.net style
    subtitle = f"Start time: {start_time_display} {timezone_label}".strip()
    title_text = event_title
    if subtitle:
        title_text = f"{event_title}<br><sub>{subtitle}</sub>"

    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor="center"),
        xaxis=dict(
            title="minutes",
            zeroline=True,
            zerolinecolor=colors["zero_baseline"],
            zerolinewidth=1,
            gridcolor=colors["grid"],
            gridwidth=0.5,
        ),
        yaxis=dict(
            title="Network Coherence (P)",
            zeroline=True,
            zerolinecolor=colors["zero_baseline"],
            zerolinewidth=1,
            gridcolor=colors["grid"],
            gridwidth=0.5,
        ),
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        height=CHART_HEIGHT,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        font=dict(family="sans-serif"),
    )

    return fig


def raw_network_chart(df: pd.DataFrame, title: str = "Raw Network Coherence") -> go.Figure:
    """Simple line chart of raw (non-cumulative) network coherence over time."""
    display_col = "datetime_display" if "datetime_display" in df.columns else "datetime_utc"

    fig = go.Figure(
        data=[go.Scatter(
            x=df[display_col],
            y=df["network_coherence"],
            mode="lines",
            name="Network Coherence",
            line=dict(color="#457B9D", width=1.5),
        )]
    )

    fig.add_hline(y=0, line_color="#999999", line_width=1, line_dash="dot")

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Network Coherence",
        template="plotly_white",
        height=CHART_HEIGHT_COMPACT,
        hovermode="x unified",
    )
    return fig


# ── Device Coherence Charts ─────────────────────────────────


def device_timeline_chart(
    df: pd.DataFrame,
    title: str = "Device Coherence",
    use_led_colors: bool = True,
    show_thresholds: bool = True,
) -> go.Figure:
    """
    Device coherence line chart with a single continuous line that
    changes color at significance transitions.

    Consecutive runs of the same significance are plotted as segments
    that overlap by one point at boundaries so the line is seamless.

    use_led_colors: True = hardware LED colors (Magenta/Cyan/Yellow/Orange/Gold)
                    False = muted print-friendly palette
    """
    colors = DEVICE_LED_COLORS if use_led_colors else DEVICE_MUTED_COLORS
    display_col = "datetime_display" if "datetime_display" in df.columns else "datetime_utc"

    fig = go.Figure()

    if df.empty:
        return fig

    sorted_df = df.sort_values(display_col).reset_index(drop=True)

    # Build segments of consecutive same-significance rows
    segments: list[tuple[str, int, int]] = []  # (significance, start_idx, end_idx)
    current_sig = sorted_df.iloc[0]["significance"]
    seg_start = 0
    for i in range(1, len(sorted_df)):
        if sorted_df.iloc[i]["significance"] != current_sig:
            segments.append((current_sig, seg_start, i - 1))
            current_sig = sorted_df.iloc[i]["significance"]
            seg_start = i
    segments.append((current_sig, seg_start, len(sorted_df) - 1))

    # Plot each segment, extending one point into neighbor for continuity
    legend_added: set[str] = set()
    for sig, s, e in segments:
        # Include one extra point on each end so segments connect
        plot_start = s if s == 0 else s - 1
        plot_end = e if e == len(sorted_df) - 1 else e + 1
        subset = sorted_df.iloc[plot_start: plot_end + 1]

        show_legend = sig not in legend_added
        legend_added.add(sig)

        fig.add_trace(go.Scatter(
            x=subset[display_col],
            y=subset["device_coherence"],
            mode="lines",
            name=sig,
            showlegend=show_legend,
            legendgroup=sig,
            line=dict(color=colors[sig], width=LINE_WIDTH_DEVICE),
            hovertemplate=(
                "Time: %{x}<br>"
                f"Coherence: %{{y:.1f}} ({sig})<extra></extra>"
            ),
        ))

    # Extreme significance background bands
    extreme_segs = [seg for seg in segments if seg[0] == "Extreme"]
    for _, s, e in extreme_segs:
        x0 = sorted_df.iloc[s][display_col]
        x1 = sorted_df.iloc[e][display_col]
        fig.add_vrect(
            x0=x0, x1=x1,
            fillcolor="rgba(255, 0, 0, 0.08)",
            line_width=0,
            layer="below",
        )

    # Peak annotation
    peak_idx = sorted_df["device_coherence"].idxmax()
    peak_row = sorted_df.iloc[peak_idx]
    peak_sig = peak_row["significance"]
    fig.add_annotation(
        x=peak_row[display_col],
        y=peak_row["device_coherence"],
        text=f"Peak: {peak_row['device_coherence']:.1f} ({peak_sig})",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowcolor="#666666",
        font=dict(size=10, color="#333333"),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#999999",
        borderwidth=1,
        yshift=10,
    )

    # Significance threshold lines
    if show_thresholds:
        for level_name, value in SIGNIFICANCE_BOUNDARY_VALUES.items():
            fig.add_hline(
                y=value,
                line_color=colors.get(level_name, "#AAAAAA"),
                line_width=LINE_WIDTH_THRESHOLD,
                line_dash="dash",
                annotation_text=f"{level_name} ({value})",
                annotation_position="top right",
                annotation_font_size=10,
                annotation_font_color="#666666",
            )

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Device Coherence",
        template="plotly_white",
        legend_title="Significance",
        height=CHART_HEIGHT,
        hovermode="x unified",
    )

    return fig


def multi_device_chart(
    frames: list[tuple[str, pd.DataFrame]],
    title: str = "Multi-Device Coherence Comparison",
) -> go.Figure:
    """
    Overlay up to 5 device coherence lines on a single chart.

    frames: list of (label, DataFrame) tuples.
    """
    fig = go.Figure()

    for idx, (label, df) in enumerate(frames):
        display_col = "datetime_display" if "datetime_display" in df.columns else "datetime_utc"
        color = MULTI_DEVICE_PALETTE[idx % len(MULTI_DEVICE_PALETTE)]

        fig.add_trace(go.Scatter(
            x=df[display_col],
            y=df["device_coherence"],
            mode="lines",
            name=label,
            line=dict(width=2, color=color),
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Device Coherence",
        template="plotly_white",
        height=CHART_HEIGHT,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return fig


# ── Correlation Charts ──────────────────────────────────────


def correlation_dual_axis_chart(
    aligned_df: pd.DataFrame,
    device_label: str = "Device",
    network_label: str = "Network",
    title: str = "Device-Network Correlation",
) -> go.Figure:
    """
    Dual-axis chart showing device coherence and network cumulative sum
    on the same time axis.

    Left Y-axis:  Device Coherence (area fill)
    Right Y-axis: Network Cumulative Sum (Red Curve + Blue Envelope)
    """
    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Device coherence as area fill (left axis)
    fig.add_trace(
        go.Scatter(
            x=aligned_df["minute_utc"],
            y=aligned_df["device_coherence"],
            mode="lines",
            name=f"{device_label} Coherence",
            line=dict(color="#457B9D", width=1.5),
            fill="tozeroy",
            fillcolor="rgba(69, 123, 157, 0.2)",
        ),
        secondary_y=False,
    )

    # Network cumsum (right axis) -- Red Curve
    fig.add_trace(
        go.Scatter(
            x=aligned_df["minute_utc"],
            y=aligned_df["network_cumsum"],
            mode="lines",
            name=f"{network_label} Cumsum",
            line=dict(color=EVENT_CHART_COLORS["red_curve"], width=LINE_WIDTH_RED_CURVE),
        ),
        secondary_y=True,
    )

    # Network envelope (right axis) -- Blue dashed
    fig.add_trace(
        go.Scatter(
            x=aligned_df["minute_utc"],
            y=aligned_df["envelope_upper"],
            mode="lines",
            name="Envelope (95% CI)",
            line=dict(color=EVENT_CHART_COLORS["blue_envelope"], width=1, dash="dash"),
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            x=aligned_df["minute_utc"],
            y=aligned_df["envelope_lower"],
            mode="lines",
            name="Envelope (95% CI)",
            line=dict(color=EVENT_CHART_COLORS["blue_envelope"], width=1, dash="dash"),
            showlegend=False,
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title=title,
        template="plotly_white",
        height=CHART_HEIGHT,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Device Coherence", secondary_y=False)
    fig.update_yaxes(title_text="Network Cumulative Sum", secondary_y=True)

    return fig
