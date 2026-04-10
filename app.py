"""
GCP2 Consciousness Data Analyzer

A free, publicly accessible web application for analyzing Random Number Generator
data from the Global Consciousness Project 2.0 (gcp2.net).
"""

import datetime

import streamlit as st

from src.constants import (
    DEFAULT_TIMEZONE,
    MAX_COMPARISON_DEVICES,
    MAX_DEVICE_UPLOADS,
    SUPPORTED_TIMEZONES,
)
from src.correlation_analysis import (
    align_device_network,
    correlation_summary,
    find_concurrent_significance,
)
from src.device_analysis import (
    detect_significant_periods,
    device_summary,
    format_significant_periods,
    significance_breakdown,
)
from src.device_config import get_all_devices, get_device_label, set_device_config
from src.network_analysis import (
    add_network_metrics,
    assess_significance,
    network_breakdown,
    network_summary,
)
from src.parsers import parse_uploaded_file
from src.plots import (
    correlation_dual_axis_chart,
    device_timeline_chart,
    multi_device_chart,
    network_event_analysis_chart,
    raw_network_chart,
)
from src.reports import (
    generate_correlation_report_pdf,
    generate_correlation_report_text,
    generate_device_report_pdf,
    generate_device_report_text,
    generate_network_report_pdf,
    generate_network_report_text,
)
from src.time_utils import (
    compute_relative_minutes,
    filter_by_date_range,
    filter_by_time_range,
    localize_for_display,
)

# ── Page Config ──────────────────────────────────────────────

st.set_page_config(
    page_title="GCP2 Consciousness Data Analyzer",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session State ────────────────────────────────────────────

if "device_datasets" not in st.session_state:
    st.session_state["device_datasets"] = {}
if "network_datasets" not in st.session_state:
    st.session_state["network_datasets"] = {}


# ── Helpers ──────────────────────────────────────────────────

def _handle_upload(files) -> None:
    for f in files:
        try:
            parsed = parse_uploaded_file(f.read(), f.name)
            if parsed.dataset_type == "device":
                label = get_device_label(parsed.device_id) if parsed.device_id else f.name
                st.session_state["device_datasets"][label] = parsed
            elif parsed.dataset_type == "network":
                label = parsed.group_name or f.name
                st.session_state["network_datasets"][label] = parsed
        except Exception as e:
            st.error(f"Error processing **{f.name}**: {e}")


def _apply_filters(df, tz, dr, tf):
    df = localize_for_display(df, tz)
    if dr and len(dr) == 2:
        df = filter_by_date_range(df, dr[0], dr[1], tz)
    if tf:
        df = filter_by_time_range(df, tf[0], tf[1])
    return df


def _date_range_str(df, tz_name):
    if df.empty:
        return ""
    col = "datetime_display" if "datetime_display" in df.columns else "datetime_utc"
    return f"{df[col].iloc[0].strftime('%Y-%m-%d %H:%M')} to {df[col].iloc[-1].strftime('%Y-%m-%d %H:%M')} {tz_name}"


# ── Sidebar ──────────────────────────────────────────────────

with st.sidebar:
    st.title("GCP2 Analyzer")
    st.caption("Consciousness Data Analysis Tool")
    st.divider()

    # Upload
    st.subheader("Upload Data")
    uploaded_files = st.file_uploader(
        "Upload CSV or ZIP files from gcp2.net",
        type=["csv", "zip"],
        accept_multiple_files=True,
        help=f"Device Coherence and/or Network Coherence (max {MAX_DEVICE_UPLOADS})",
    )
    if uploaded_files:
        _handle_upload(uploaded_files)

    device_count = len(st.session_state["device_datasets"])
    network_count = len(st.session_state["network_datasets"])

    if device_count > 0 or network_count > 0:
        st.divider()
        st.subheader("Loaded Files")
        if device_count > 0:
            st.markdown("**Devices:**")
            for label, ds in st.session_state["device_datasets"].items():
                st.markdown(f"- {label} ({ds.row_count:,} rows)")
        if network_count > 0:
            st.markdown("**Network:**")
            for label, ds in st.session_state["network_datasets"].items():
                st.markdown(f"- {label} ({ds.row_count:,} rows)")
        if st.button("Clear All Data"):
            st.session_state["device_datasets"] = {}
            st.session_state["network_datasets"] = {}
            st.rerun()

    st.divider()
    st.subheader("Settings")
    timezone = st.selectbox("Display Timezone", SUPPORTED_TIMEZONES, index=SUPPORTED_TIMEZONES.index(DEFAULT_TIMEZONE))

    date_range = None
    time_filter = None

    if device_count > 0 or network_count > 0:
        st.divider()
        st.subheader("Filters")
        all_dates = []
        for ds in list(st.session_state["device_datasets"].values()) + list(st.session_state["network_datasets"].values()):
            if ds.date_min:
                all_dates.append(ds.date_min)
            if ds.date_max:
                all_dates.append(ds.date_max)
        if all_dates:
            overall_min = min(all_dates).date()
            overall_max = max(all_dates).date()
            date_range = st.date_input("Date Range", value=(overall_min, overall_max), min_value=overall_min, max_value=overall_max)
        use_time = st.checkbox("Filter by time of day")
        if use_time:
            start_time = st.time_input("Start time", datetime.time(0, 0))
            end_time = st.time_input("End time", datetime.time(23, 59))
            time_filter = (start_time, end_time)

    st.divider()
    st.subheader("Device Names")
    existing_devices = get_all_devices()
    if existing_devices:
        for did, info in existing_devices.items():
            st.text(f"Device {did}: {info.get('name', '—')}")
    with st.expander("Add / Edit Device Name"):
        new_id = st.number_input("Device ID", min_value=1, step=1, value=15)
        new_name = st.text_input("Name", placeholder="e.g., Lab1")
        new_loc = st.text_input("Location", placeholder="e.g., California")
        if st.button("Save Name") and new_name:
            set_device_config(int(new_id), new_name, new_loc)
            st.success(f"Saved: Device {new_id} = {new_name}")
            st.rerun()


# ── Main Content ─────────────────────────────────────────────

has_data = device_count > 0 or network_count > 0

if not has_data:
    st.title("GCP2 Consciousness Data Analyzer")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
### Welcome

This tool analyzes RNG data from the **Global Consciousness Project 2.0**.

**Getting Started:**
1. Go to [gcp2.net](https://gcp2.net) > Data & Results > Data Download
2. Download **Device Coherence** CSV for your device(s)
3. Download **Network Coherence** CSV for the time period to analyze
4. Upload the files using the sidebar

**What This Tool Can Do:**
- Analyze device coherence and identify significant periods
- Generate Event Analysis charts (Red Curve + Blue Envelope)
- Compare multiple devices side by side
- Correlate device activity with network coherence
- Generate detailed PDF reports and export charts
        """)
    with col2:
        st.markdown("""
### About the Data

GCP 2.0 collects quantum random data from **NextGen RNG devices**
hosted by citizen scientists worldwide.

**Device Coherence** measures whether RNGs inside a single device
are synchronizing beyond what chance allows.

**Network Coherence** measures whether devices across the global
network are synchronizing -- potentially reflecting shared human
consciousness.

When the **Red Curve** exits the **Blue Envelope**, the network
is behaving in a way that would happen less than 5% of the time
by pure chance (p < 0.05).
        """)
    st.info("Upload CSV files from gcp2.net using the sidebar to begin.")

else:
    st.title("GCP2 Consciousness Data Analyzer")

    # Warnings
    for label, ds in {**st.session_state["device_datasets"], **st.session_state["network_datasets"]}.items():
        for w in ds.warnings:
            st.warning(f"**{label}:** {w}")

    # Build tabs
    tab_names = []
    if device_count > 0:
        tab_names.append("Device Analysis")
    if network_count > 0:
        tab_names.append("Network Analysis")
    if device_count > 0 and network_count > 0:
        tab_names.append("Correlation")

    tabs = st.tabs(tab_names)
    tab_idx = 0

    # ══════════════════════════════════════════════════════════
    # DEVICE ANALYSIS TAB
    # ══════════════════════════════════════════════════════════
    if device_count > 0:
        with tabs[tab_idx]:
            st.header("Device Coherence Analysis")

            for label, ds in st.session_state["device_datasets"].items():
                st.subheader(label)
                filtered = _apply_filters(ds.df, timezone, date_range, time_filter)

                if filtered.empty:
                    st.warning("No data in the selected range.")
                    continue

                summary = device_summary(filtered)
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Rows", f"{summary['rows']:,}")
                c2.metric("Mean", f"{summary['mean_coherence']}")
                c3.metric("Max", f"{summary['max_coherence']} ({summary['max_significance']})")
                c4.metric("Elevated+", f"{summary['elevated_rows']:,}")
                c5.metric("Coverage", f"{summary['coverage_pct']}%")

                dev_tabs = st.tabs(["Timeline Chart", "Significance", "Significant Periods", "Report"])

                # ── Timeline Chart ───────────────────────────
                with dev_tabs[0]:
                    use_led = st.checkbox("LED colors (hardware match)", value=True, key=f"led_{label}")
                    fig = device_timeline_chart(filtered, title=label, use_led_colors=use_led)
                    st.plotly_chart(fig, use_container_width=True)

                    ca, cb = st.columns(2)
                    with ca:
                        png = fig.to_image(format="png", width=1600, height=900, scale=2)
                        st.download_button("Download Chart (PNG)", data=png,
                            file_name=f"GCP2_{label.replace(' ', '_')}_chart.png",
                            mime="image/png", key=f"dpng_{label}")
                    with cb:
                        csv = filtered.to_csv(index=False).encode("utf-8")
                        st.download_button("Download Data (CSV)", data=csv,
                            file_name=f"GCP2_{label.replace(' ', '_')}_data.csv",
                            mime="text/csv", key=f"dcsv_{label}")

                # ── Significance Breakdown ────────────────────
                with dev_tabs[1]:
                    bd = significance_breakdown(filtered)
                    st.dataframe(bd, use_container_width=True, hide_index=True)

                # ── Significant Periods ───────────────────────
                with dev_tabs[2]:
                    periods = detect_significant_periods(filtered)
                    if periods:
                        st.text(format_significant_periods(periods))
                    else:
                        st.info("No periods of elevated significance in this range.")

                # ── Report Generation ─────────────────────────
                with dev_tabs[3]:
                    bd = significance_breakdown(filtered)
                    periods = detect_significant_periods(filtered)
                    dr_str = _date_range_str(filtered, timezone)

                    report_text = generate_device_report_text(
                        label, summary, bd, periods, dr_str, timezone
                    )
                    st.text_area("Report Preview", report_text, height=400, key=f"drpt_{label}")

                    rca, rcb = st.columns(2)
                    with rca:
                        st.download_button("Download Report (TXT)", data=report_text,
                            file_name=f"GCP2_{label.replace(' ', '_')}_report.txt",
                            mime="text/plain", key=f"dtxt_{label}")
                    with rcb:
                        chart_png = fig.to_image(format="png", width=1600, height=900, scale=2)
                        pdf_bytes = generate_device_report_pdf(
                            label, summary, bd, periods, dr_str, timezone, chart_png
                        )
                        st.download_button("Download Report (PDF)", data=pdf_bytes,
                            file_name=f"GCP2_{label.replace(' ', '_')}_report.pdf",
                            mime="application/pdf", key=f"dpdf_{label}")

                st.divider()

            # Multi-device comparison
            if device_count >= 2:
                st.subheader("Multi-Device Comparison")
                selected = st.multiselect(
                    "Select devices to compare",
                    list(st.session_state["device_datasets"].keys()),
                    default=list(st.session_state["device_datasets"].keys())[:MAX_COMPARISON_DEVICES],
                    max_selections=MAX_COMPARISON_DEVICES,
                )
                if len(selected) >= 2:
                    frames = [(lbl, _apply_filters(st.session_state["device_datasets"][lbl].df, timezone, date_range, time_filter)) for lbl in selected]
                    fig = multi_device_chart(frames)
                    st.plotly_chart(fig, use_container_width=True)
                    png = fig.to_image(format="png", width=1600, height=900, scale=2)
                    st.download_button("Download Comparison (PNG)", data=png,
                        file_name="GCP2_MultiDevice_Comparison.png", mime="image/png")

        tab_idx += 1

    # ══════════════════════════════════════════════════════════
    # NETWORK ANALYSIS TAB
    # ══════════════════════════════════════════════════════════
    if network_count > 0:
        with tabs[tab_idx]:
            st.header("Network Coherence Analysis")

            for label, ds in st.session_state["network_datasets"].items():
                st.subheader(label)
                filtered = _apply_filters(ds.df, timezone, date_range, time_filter)

                if filtered.empty:
                    st.warning("No data in the selected range.")
                    continue

                st.markdown(f"**{len(filtered):,}** data points ({len(filtered)/60:.0f} minutes)")

                # Event metadata
                st.markdown("#### Event Details")
                ec1, ec2 = st.columns(2)
                with ec1:
                    event_title = st.text_input("Event Title", value="Event Analysis", key=f"et_{label}")
                with ec2:
                    event_start_str = st.text_input("Event Start (optional)", placeholder="YYYY-MM-DD HH:MM:SS", key=f"es_{label}")

                # Determine start epoch
                if event_start_str:
                    try:
                        import pytz
                        tz = pytz.timezone(timezone)
                        naive = datetime.datetime.strptime(event_start_str, "%Y-%m-%d %H:%M:%S")
                        event_start_epoch = int(tz.localize(naive).timestamp())
                    except Exception:
                        st.warning("Could not parse start time. Using first data point.")
                        event_start_epoch = int(filtered["epoch_time_utc"].iloc[0])
                else:
                    event_start_epoch = int(filtered["epoch_time_utc"].iloc[0])

                # Compute metrics
                metrics_df = add_network_metrics(filtered)
                metrics_df = compute_relative_minutes(metrics_df, event_start_epoch)

                start_display = filtered["datetime_display"].iloc[0].strftime("%Y-%m-%d %H:%M:%S")
                tz_abbrev = filtered["datetime_display"].iloc[0].strftime("%Z")

                net_tabs = st.tabs(["Event Analysis Chart", "Raw Coherence", "Summary & Assessment", "Report"])

                # ── Event Analysis Chart ──────────────────────
                with net_tabs[0]:
                    fig = network_event_analysis_chart(metrics_df, event_title, start_display, tz_abbrev)
                    st.plotly_chart(fig, use_container_width=True)

                    na, nb = st.columns(2)
                    with na:
                        png = fig.to_image(format="png", width=1600, height=900, scale=2)
                        st.download_button("Download Chart (PNG)", data=png,
                            file_name=f"GCP2_EventAnalysis_{event_title.replace(' ', '_')}.png",
                            mime="image/png", key=f"npng_{label}")
                    with nb:
                        csv = metrics_df.to_csv(index=False).encode("utf-8")
                        st.download_button("Download Data (CSV)", data=csv,
                            file_name=f"GCP2_Network_{label.replace(' ', '_')}_analysis.csv",
                            mime="text/csv", key=f"ncsv_{label}")

                # ── Raw Coherence ─────────────────────────────
                with net_tabs[1]:
                    fig_raw = raw_network_chart(filtered, title=f"{label} - Raw Coherence")
                    st.plotly_chart(fig_raw, use_container_width=True)

                # ── Summary & Assessment ──────────────────────
                with net_tabs[2]:
                    ns = network_summary(metrics_df)

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Duration", f"{ns['duration_minutes']} min")
                    c2.metric("Final Cumsum", f"{ns['final_cumsum']:+.1f}" if ns['final_cumsum'] is not None else "—")
                    c3.metric("Peak Cumsum", f"{ns['peak_cumsum']:+.1f}" if ns['peak_cumsum'] is not None else "—")
                    c4.metric("Active Devices", ns['active_devices_range'] or "—")

                    st.markdown("#### Significance Assessment")
                    assessment = assess_significance(ns)
                    if ns.get("envelope_exit"):
                        st.success(assessment)
                    else:
                        st.info(assessment)

                    st.markdown("#### Coherence Breakdown")
                    bd = network_breakdown(filtered)
                    bc1, bc2, bc3 = st.columns(3)
                    bc1.metric("Positive Rows", f"{bd['positive_rows']:,}")
                    bc2.metric("Negative Rows", f"{bd['negative_rows']:,}")
                    bc3.metric("Largest (+/-)",
                        f"+{bd['largest_positive']:.4f} / {bd['largest_negative']:.4f}" if bd['largest_positive'] is not None else "—")

                # ── Report ────────────────────────────────────
                with net_tabs[3]:
                    ns = network_summary(metrics_df)
                    assessment = assess_significance(ns)
                    dr_str = _date_range_str(filtered, timezone)

                    report_text = generate_network_report_text(
                        label, ns, assessment, event_title, dr_str, timezone
                    )
                    st.text_area("Report Preview", report_text, height=400, key=f"nrpt_{label}")

                    ra, rb = st.columns(2)
                    with ra:
                        st.download_button("Download Report (TXT)", data=report_text,
                            file_name=f"GCP2_Network_{label.replace(' ', '_')}_report.txt",
                            mime="text/plain", key=f"ntxt_{label}")
                    with rb:
                        chart_png = fig.to_image(format="png", width=1600, height=900, scale=2)
                        pdf_bytes = generate_network_report_pdf(
                            label, ns, assessment, event_title, dr_str, timezone, chart_png
                        )
                        st.download_button("Download Report (PDF)", data=pdf_bytes,
                            file_name=f"GCP2_Network_{label.replace(' ', '_')}_report.pdf",
                            mime="application/pdf", key=f"npdf_{label}")

                st.divider()

        tab_idx += 1

    # ══════════════════════════════════════════════════════════
    # CORRELATION TAB
    # ══════════════════════════════════════════════════════════
    if device_count > 0 and network_count > 0:
        with tabs[tab_idx]:
            st.header("Device-Network Correlation")

            # Select which device and network to correlate
            dev_labels = list(st.session_state["device_datasets"].keys())
            net_labels = list(st.session_state["network_datasets"].keys())

            cc1, cc2 = st.columns(2)
            with cc1:
                sel_device = st.selectbox("Select Device", dev_labels, key="corr_dev")
            with cc2:
                sel_network = st.selectbox("Select Network", net_labels, key="corr_net")

            dev_ds = st.session_state["device_datasets"][sel_device]
            net_ds = st.session_state["network_datasets"][sel_network]

            dev_filtered = _apply_filters(dev_ds.df, timezone, date_range, time_filter)
            net_filtered = _apply_filters(net_ds.df, timezone, date_range, time_filter)

            if dev_filtered.empty or net_filtered.empty:
                st.warning("One or both datasets have no data in the selected range.")
            else:
                # Align data
                aligned = align_device_network(dev_filtered, net_filtered)

                if aligned.empty:
                    st.warning("No overlapping time range between the selected device and network data. Check your date filters.")
                else:
                    st.markdown(f"**{len(aligned)}** overlapping minutes found.")

                    # Concurrent significance
                    concurrent = find_concurrent_significance(aligned)
                    corr_sum = correlation_summary(aligned, concurrent, sel_device, sel_network)

                    # Summary metrics
                    mc1, mc2, mc3, mc4 = st.columns(4)
                    mc1.metric("Overlap", f"{corr_sum['overlap_minutes']} min")
                    mc2.metric("Device Elevated+", f"{corr_sum['device_elevated_minutes']} min")
                    mc3.metric("Network Significant", f"{corr_sum['network_significant_minutes']} min")
                    mc4.metric("Concurrent", f"{corr_sum['concurrent_minutes']} min ({corr_sum['period_count']} windows)")

                    corr_tabs = st.tabs(["Correlation Chart", "Concurrent Periods", "Report"])

                    # ── Correlation Chart ─────────────────────
                    with corr_tabs[0]:
                        fig = correlation_dual_axis_chart(aligned, sel_device, sel_network)
                        st.plotly_chart(fig, use_container_width=True)

                        ca, cb = st.columns(2)
                        with ca:
                            png = fig.to_image(format="png", width=1600, height=900, scale=2)
                            st.download_button("Download Chart (PNG)", data=png,
                                file_name="GCP2_Correlation_Chart.png",
                                mime="image/png", key="corr_png")
                        with cb:
                            csv = aligned.to_csv(index=False).encode("utf-8")
                            st.download_button("Download Aligned Data (CSV)", data=csv,
                                file_name="GCP2_Correlation_Data.csv",
                                mime="text/csv", key="corr_csv")

                    # ── Concurrent Periods ────────────────────
                    with corr_tabs[1]:
                        if concurrent:
                            for i, p in enumerate(concurrent[:10], 1):
                                st.markdown(
                                    f"**{i}. {p['start_time']} to {p['end_time']}** ({p['duration_minutes']} min)\n\n"
                                    f"- Device peak: {p['device_peak']} ({p['device_peak_significance']})\n"
                                    f"- Network cumsum: {p['network_cumsum_peak']:+.1f} ({p['network_direction']})"
                                )
                        else:
                            st.info("No periods of simultaneous device + network significance found in this range.")

                    # ── Report ────────────────────────────────
                    with corr_tabs[2]:
                        dr_str = _date_range_str(dev_filtered, timezone)
                        report_text = generate_correlation_report_text(
                            corr_sum, concurrent, dr_str, timezone
                        )
                        st.text_area("Report Preview", report_text, height=400, key="corr_rpt")

                        ra, rb = st.columns(2)
                        with ra:
                            st.download_button("Download Report (TXT)", data=report_text,
                                file_name="GCP2_Correlation_Report.txt",
                                mime="text/plain", key="corr_txt")
                        with rb:
                            chart_png = fig.to_image(format="png", width=1600, height=900, scale=2)
                            pdf_bytes = generate_correlation_report_pdf(
                                corr_sum, concurrent, dr_str, timezone, chart_png
                            )
                            st.download_button("Download Report (PDF)", data=pdf_bytes,
                                file_name="GCP2_Correlation_Report.pdf",
                                mime="application/pdf", key="corr_pdf")
