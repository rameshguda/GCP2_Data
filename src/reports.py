"""
Report generation for GCP2 Consciousness Data Analyzer.

Generates structured text reports and PDF documents for:
  - Device Activity Reports
  - Network Coherence Analysis Reports
  - Device-Network Correlation Reports

PDF generation uses fpdf2.
"""

from __future__ import annotations

import io
from datetime import datetime, timezone

from fpdf import FPDF

from src.constants import SIGNIFICANCE_ORDER


class GCP2Report(FPDF):
    """Custom PDF with GCP2 branding and footer."""

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(23, 42, 58)  # Dark slate #172A3A
        self.cell(0, 8, "GCP2 Consciousness Data Analyzer", new_x="LMARGIN", new_y="NEXT", align="R")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Data source: gcp2.net", align="C")


def _add_section(pdf: GCP2Report, title: str):
    """Add a section header to the PDF."""
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(193, 18, 31)  # HeartMath burgundy #C1121F
    pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(23, 42, 58)
    pdf.ln(2)


def _add_body(pdf: GCP2Report, text: str):
    """Add body text to the PDF."""
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, text)
    pdf.ln(2)


def _add_metric_row(pdf: GCP2Report, label: str, value: str):
    """Add a label: value row."""
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(60, 6, label + ":")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, str(value), new_x="LMARGIN", new_y="NEXT")


def _add_table(pdf: GCP2Report, headers: list[str], rows: list[list[str]], col_widths: list[int] | None = None):
    """Add a simple table to the PDF."""
    if col_widths is None:
        col_widths = [int(190 / len(headers))] * len(headers)

    # Header row
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(233, 240, 245)  # Light blue-gray
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, h, border=1, fill=True)
    pdf.ln()

    # Data rows
    pdf.set_font("Helvetica", "", 9)
    for row in rows:
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 6, str(cell), border=1)
        pdf.ln()
    pdf.ln(3)


# ── Device Activity Report ───────────────────────────────────

def generate_device_report_text(
    device_label: str,
    summary: dict,
    breakdown_df,
    periods: list[dict],
    date_range_str: str = "",
    timezone_str: str = "UTC",
) -> str:
    """Generate a plain-text Device Activity Report."""
    lines = [
        "=" * 65,
        "DEVICE ACTIVITY REPORT",
        "=" * 65,
        f"Device:     {device_label}",
        f"Period:     {date_range_str}",
        f"Timezone:   {timezone_str}",
        f"Generated:  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Data Rows:  {summary['rows']:,}",
        f"Coverage:   {summary['coverage_pct']}%",
        "-" * 65,
        "",
        "SUMMARY STATISTICS",
        "-" * 20,
        f"Mean Device Coherence:    {summary['mean_coherence']}",
        f"Max Device Coherence:     {summary['max_coherence']} ({summary['max_significance']})",
        f"Min Device Coherence:     {summary['min_coherence']}",
        "",
        "SIGNIFICANCE BREAKDOWN",
        "-" * 23,
    ]

    for _, row in breakdown_df.iterrows():
        lines.append(
            f"  {row['significance']:12s}  {int(row['rows']):>6,} rows  ({row['percent']:5.1f}%)  {row['p_value']}"
        )

    lines.append("")
    lines.append("SIGNIFICANT PERIODS")
    lines.append("-" * 20)

    if not periods:
        lines.append("  No periods of elevated significance detected.")
    else:
        shown = min(len(periods), 15)
        lines.append(f"Top {shown} periods (of {len(periods)} total):")
        lines.append("")
        for i, p in enumerate(periods[:shown], 1):
            lines.append(f"  {i}. {p['start_time']} to {p['end_time']}")
            lines.append(f"     Peak: {p['peak_value']} ({p['peak_significance']}) at {p['peak_time']}")
            lines.append(f"     Duration: {p['duration_minutes']} min, Active seconds: {p['mean_active_seconds']:.0f}")
            lines.append("")

    lines.append("=" * 65)
    return "\n".join(lines)


def generate_device_report_pdf(
    device_label: str,
    summary: dict,
    breakdown_df,
    periods: list[dict],
    date_range_str: str = "",
    timezone_str: str = "UTC",
    chart_png: bytes | None = None,
) -> bytes:
    """Generate a PDF Device Activity Report."""
    pdf = GCP2Report()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(193, 18, 31)
    pdf.cell(0, 12, "Device Activity Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(23, 42, 58)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, device_label, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6, date_range_str, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)

    # Summary
    _add_section(pdf, "Summary Statistics")
    _add_metric_row(pdf, "Data Rows", f"{summary['rows']:,}")
    _add_metric_row(pdf, "Coverage", f"{summary['coverage_pct']}%")
    _add_metric_row(pdf, "Mean Coherence", str(summary['mean_coherence']))
    _add_metric_row(pdf, "Max Coherence", f"{summary['max_coherence']} ({summary['max_significance']})")
    _add_metric_row(pdf, "Min Coherence", str(summary['min_coherence']))
    _add_metric_row(pdf, "Elevated+ Rows", f"{summary['elevated_rows']:,}")
    pdf.ln(4)

    # Breakdown table
    _add_section(pdf, "Significance Breakdown")
    headers = ["Level", "Rows", "Percent", "p-value"]
    rows = []
    for _, row in breakdown_df.iterrows():
        rows.append([
            row["significance"],
            f"{int(row['rows']):,}",
            f"{row['percent']:.1f}%",
            row["p_value"],
        ])
    _add_table(pdf, headers, rows, [50, 40, 40, 60])

    # Chart image
    if chart_png:
        _add_section(pdf, "Device Coherence Timeline")
        img_stream = io.BytesIO(chart_png)
        pdf.image(img_stream, x=10, w=190)
        pdf.ln(4)

    # Significant periods
    if periods:
        _add_section(pdf, "Significant Periods")
        shown = min(len(periods), 15)
        headers = ["#", "Start", "End", "Peak", "Level", "Duration"]
        rows = []
        for i, p in enumerate(periods[:shown], 1):
            rows.append([
                str(i),
                str(p["start_time"])[:19],
                str(p["end_time"])[:19],
                str(p["peak_value"]),
                p["peak_significance"],
                f"{p['duration_minutes']} min",
            ])
        _add_table(pdf, headers, rows, [10, 45, 45, 30, 30, 30])

    # Footer note
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4,
        "Generated by GCP2 Consciousness Data Analyzer. "
        "Data source: gcp2.net. Statistical methodology follows Bancel & Nelson (2008)."
    )

    return bytes(pdf.output())


# ── Network Analysis Report ──────────────────────────────────

def generate_network_report_text(
    network_label: str,
    summary: dict,
    assessment: str,
    event_title: str = "",
    date_range_str: str = "",
    timezone_str: str = "UTC",
) -> str:
    """Generate a plain-text Network Coherence Analysis Report."""
    lines = [
        "=" * 65,
        "NETWORK COHERENCE ANALYSIS REPORT",
        "=" * 65,
        f"Network:    {network_label}",
        f"Event:      {event_title}" if event_title else "",
        f"Period:     {date_range_str}",
        f"Duration:   {summary['duration_minutes']} minutes ({summary['duration_seconds']} seconds)",
        f"Timezone:   {timezone_str}",
        f"Generated:  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Data Points: {summary['data_points']:,}",
        f"Active Devices: {summary['active_devices_range']}",
        "-" * 65,
        "",
        "CUMULATIVE SUM ANALYSIS",
        "-" * 24,
        f"Final Cumulative Value:  {summary['final_cumsum']:+.1f}" if summary['final_cumsum'] is not None else "",
        f"Peak Cumulative Value:   {summary['peak_cumsum']:+.1f} at minute {summary['peak_cumsum_minute']}" if summary['peak_cumsum'] is not None else "",
        f"Min Cumulative Value:    {summary['min_cumsum']:+.1f} at minute {summary['min_cumsum_minute']}" if summary['min_cumsum'] is not None else "",
        "",
        "SIGNIFICANCE ASSESSMENT",
        "-" * 24,
        assessment,
        "",
    ]

    exit_info = summary.get("envelope_exit")
    if exit_info:
        lines.extend([
            "ENVELOPE EXIT DETAILS",
            "-" * 22,
            f"Direction:     {exit_info['direction']} boundary",
            f"Exit Second:   {exit_info['second']}",
            f"Exit Minute:   {exit_info['minute']:.1f}",
            f"Cumsum Value:  {exit_info['cumsum_value']:+.1f}",
            "",
        ])

    lines.append("=" * 65)
    return "\n".join([l for l in lines if l is not None])


def generate_network_report_pdf(
    network_label: str,
    summary: dict,
    assessment: str,
    event_title: str = "",
    date_range_str: str = "",
    timezone_str: str = "UTC",
    chart_png: bytes | None = None,
) -> bytes:
    """Generate a PDF Network Coherence Analysis Report."""
    pdf = GCP2Report()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(193, 18, 31)
    pdf.cell(0, 12, "Network Coherence Analysis", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(23, 42, 58)
    pdf.set_font("Helvetica", "", 12)
    if event_title:
        pdf.cell(0, 8, event_title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6, f"{network_label} | {date_range_str}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)

    # Summary
    _add_section(pdf, "Analysis Summary")
    _add_metric_row(pdf, "Duration", f"{summary['duration_minutes']} minutes ({summary['data_points']:,} data points)")
    _add_metric_row(pdf, "Active Devices", str(summary['active_devices_range']))
    _add_metric_row(pdf, "Mean Coherence", str(summary['mean_coherence']))
    if summary['final_cumsum'] is not None:
        _add_metric_row(pdf, "Final Cumulative Sum", f"{summary['final_cumsum']:+.1f}")
        _add_metric_row(pdf, "Peak Cumulative Sum", f"{summary['peak_cumsum']:+.1f} (minute {summary['peak_cumsum_minute']})")
    pdf.ln(4)

    # Significance
    _add_section(pdf, "Significance Assessment")
    exit_info = summary.get("envelope_exit")
    if exit_info:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 7, "STATISTICALLY SIGNIFICANT", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(23, 42, 58)
        pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, assessment)

    # Chart
    if chart_png:
        _add_section(pdf, "Event Analysis Chart")
        img_stream = io.BytesIO(chart_png)
        pdf.image(img_stream, x=10, w=190)
        pdf.ln(4)

    # Footer
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4,
        "Generated by GCP2 Consciousness Data Analyzer. "
        "Data source: gcp2.net. The Blue Envelope represents the 95% confidence "
        "interval of chi-squared data with degrees of freedom equal to elapsed seconds. "
        "Methodology follows Bancel & Nelson (2008), Journal of Scientific Exploration."
    )

    return bytes(pdf.output())


# ── Correlation Report ───────────────────────────────────────

def generate_correlation_report_text(
    corr_summary: dict,
    concurrent_periods: list[dict],
    date_range_str: str = "",
    timezone_str: str = "UTC",
) -> str:
    """Generate a plain-text Device-Network Correlation Report."""
    lines = [
        "=" * 65,
        "DEVICE-NETWORK CORRELATION REPORT",
        "=" * 65,
        f"Device:     {corr_summary['device_label']}",
        f"Network:    {corr_summary['network_label']}",
        f"Period:     {date_range_str}",
        f"Timezone:   {timezone_str}",
        f"Generated:  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "-" * 65,
        "",
        "TEMPORAL CORRELATION SUMMARY",
        "-" * 28,
        f"Overlapping minutes:           {corr_summary['overlap_minutes']}",
        f"Device elevated+ minutes:      {corr_summary['device_elevated_minutes']}",
        f"Network significant minutes:   {corr_summary['network_significant_minutes']}",
        f"Concurrent significance:       {corr_summary['concurrent_minutes']} minutes",
        "",
    ]

    if corr_summary['concurrent_minutes'] > 0:
        lines.extend([
            f"Of the device's {corr_summary['device_elevated_minutes']} elevated minutes, "
            f"{corr_summary['concurrent_pct_of_device']:.0f}% coincided with network significance.",
            "",
        ])

    lines.append("CONCURRENT SIGNIFICANCE WINDOWS")
    lines.append("-" * 31)

    if not concurrent_periods:
        lines.append("  No periods of simultaneous device + network significance found.")
    else:
        for i, p in enumerate(concurrent_periods[:10], 1):
            lines.append(f"  {i}. {p['start_time']} to {p['end_time']} ({p['duration_minutes']} min)")
            lines.append(f"     Device peak: {p['device_peak']} ({p['device_peak_significance']})")
            lines.append(f"     Network cumsum peak: {p['network_cumsum_peak']:+.1f} ({p['network_direction']})")
            lines.append("")

    lines.append("=" * 65)
    return "\n".join(lines)


def generate_correlation_report_pdf(
    corr_summary: dict,
    concurrent_periods: list[dict],
    date_range_str: str = "",
    timezone_str: str = "UTC",
    chart_png: bytes | None = None,
) -> bytes:
    """Generate a PDF Correlation Report."""
    pdf = GCP2Report()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(193, 18, 31)
    pdf.cell(0, 12, "Device-Network Correlation", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(23, 42, 58)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"{corr_summary['device_label']}  vs  {corr_summary['network_label']}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6, date_range_str, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)

    # Summary
    _add_section(pdf, "Correlation Summary")
    _add_metric_row(pdf, "Overlapping Minutes", str(corr_summary['overlap_minutes']))
    _add_metric_row(pdf, "Device Elevated+ Minutes", str(corr_summary['device_elevated_minutes']))
    _add_metric_row(pdf, "Network Significant Minutes", str(corr_summary['network_significant_minutes']))
    _add_metric_row(pdf, "Concurrent Significance", f"{corr_summary['concurrent_minutes']} minutes ({corr_summary['period_count']} windows)")
    if corr_summary['device_elevated_minutes'] > 0:
        _add_metric_row(pdf, "Overlap Rate (of device)", f"{corr_summary['concurrent_pct_of_device']:.0f}%")
    pdf.ln(4)

    # Chart
    if chart_png:
        _add_section(pdf, "Correlation Chart")
        img_stream = io.BytesIO(chart_png)
        pdf.image(img_stream, x=10, w=190)
        pdf.ln(4)

    # Periods table
    if concurrent_periods:
        _add_section(pdf, "Concurrent Significance Windows")
        headers = ["#", "Start", "End", "Duration", "Device Peak", "Net Cumsum"]
        rows = []
        for i, p in enumerate(concurrent_periods[:10], 1):
            rows.append([
                str(i),
                str(p["start_time"])[:16],
                str(p["end_time"])[:16],
                f"{p['duration_minutes']} min",
                f"{p['device_peak']} ({p['device_peak_significance']})",
                f"{p['network_cumsum_peak']:+.1f}",
            ])
        _add_table(pdf, headers, rows, [10, 38, 38, 24, 45, 35])

    # Footer
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4,
        "Generated by GCP2 Consciousness Data Analyzer. Data source: gcp2.net."
    )

    return bytes(pdf.output())
