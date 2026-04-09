from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.device_analysis import SIGNIFICANCE_COLORS
from src.network_analysis import add_network_metrics


def device_line_figure(df: pd.DataFrame, title: str) -> go.Figure:
    figure = go.Figure()
    for significance, color in SIGNIFICANCE_COLORS.items():
        subset = df[df["significance"] == significance]
        if subset.empty:
            continue
        figure.add_trace(
            go.Scatter(
                x=subset["datetime_display"],
                y=subset["device_coherence"],
                mode="markers+lines",
                name=significance,
                marker={"color": color, "size": 6},
                line={"color": color, "width": 1},
            )
        )
    figure.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Device Coherence",
        template="plotly_white",
        legend_title="Significance",
        height=520,
        hovermode="x unified",
    )
    return figure


def multi_device_figure(frames: list[tuple[str, pd.DataFrame]]) -> go.Figure:
    figure = go.Figure()
    palette = ["#1D3557", "#457B9D", "#E76F51", "#2A9D8F"]
    for idx, (label, df) in enumerate(frames):
        figure.add_trace(
            go.Scatter(
                x=df["datetime_display"],
                y=df["device_coherence"],
                mode="lines",
                name=label,
                line={"width": 2, "color": palette[idx % len(palette)]},
            )
        )
    figure.update_layout(
        title="Multi-Device Coherence Comparison",
        xaxis_title="Time",
        yaxis_title="Device Coherence",
        template="plotly_white",
        height=520,
        hovermode="x unified",
    )
    return figure


def network_cumsum_figure(df: pd.DataFrame, title: str) -> go.Figure:
    metrics = add_network_metrics(df)
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=metrics["datetime_display"],
            y=metrics["cumulative_coherence"],
            mode="lines",
            name="Cumulative Coherence",
            line={"color": "#C1121F", "width": 2},
        )
    )
    figure.add_hline(y=0, line_color="#999999", line_width=1, line_dash="dot")
    figure.add_trace(
        go.Scatter(
            x=metrics["datetime_display"],
            y=metrics["envelope_upper"],
            mode="lines",
            name="Envelope Upper",
            line={"color": "#1D3557", "width": 1.5},
        )
    )
    figure.add_trace(
        go.Scatter(
            x=metrics["datetime_display"],
            y=metrics["envelope_lower"],
            mode="lines",
            name="Envelope Lower",
            line={"color": "#1D3557", "width": 1.5},
        )
    )
    figure.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Cumulative Network Coherence",
        template="plotly_white",
        height=520,
        hovermode="x unified",
    )
    return figure


def raw_network_figure(df: pd.DataFrame, title: str) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Scatter(
                x=df["datetime_display"],
                y=df["network_coherence"],
                mode="lines",
                name="Network Coherence",
                line={"color": "#457B9D", "width": 1.5},
            )
        ]
    )
    figure.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Network Coherence",
        template="plotly_white",
        height=420,
        hovermode="x unified",
    )
    return figure
