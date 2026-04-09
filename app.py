from __future__ import annotations

from datetime import time
from pathlib import Path

import pandas as pd
import streamlit as st

from src.demo_data import load_demo_datasets
from src.device_analysis import device_summary, significance_breakdown
from src.network_analysis import network_breakdown, network_summary
from src.parsers import ParsedDataset, parse_uploaded_file
from src.plots import (
    device_line_figure,
    multi_device_figure,
    network_cumsum_figure,
    raw_network_figure,
)
from src.quality import detect_quality_issues
from src.storage import save_analysis_record
from src.summaries import build_device_summary_text, build_network_summary_text
from src.time_utils import filter_by_date_and_time

st.set_page_config(page_title="GCP2 Data Analysis App", layout="wide")

ANALYSIS_DIR = Path("saved_analyses")


def figure_download_bytes(figure) -> bytes | None:
    try:
        return figure.to_image(format="png")
    except Exception:
        return None


def render_dataset_overview(dataset: ParsedDataset) -> None:
    df = dataset.dataframe
    st.write(f"Type: `{dataset.data_type}`")
    st.write(f"Rows: `{len(df):,}`")
    st.write(f"UTC range: `{df['datetime_utc'].min()}` to `{df['datetime_utc'].max()}`")
    if dataset.device_id:
        st.write(f"Device ID: `{dataset.device_id}`")
    if dataset.group_name:
        st.write(f"Group: `{dataset.group_name}`")


def show_quality_issues(dataset: ParsedDataset) -> None:
    issues = detect_quality_issues(dataset.dataframe, dataset.data_type)
    for issue in issues:
        st.warning(issue, icon="!")


def dataset_option_label(dataset: ParsedDataset) -> str:
    return f"{dataset.source_label} ({dataset.data_type})"


def render_summary_metrics(label: str, summary: dict[str, object], data_type: str) -> None:
    if data_type == "device":
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", f"{summary['rows']:,}")
        col2.metric("Mean coherence", f"{summary['mean_coherence']:.2f}" if summary["mean_coherence"] is not None else "-")
        col3.metric("Max coherence", f"{summary['max_coherence']:.2f}" if summary["max_coherence"] is not None else "-")
        col4.metric("Coverage", f"{summary['coverage_pct']:.1f}%" if summary["coverage_pct"] is not None else "-")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", f"{summary['rows']:,}")
        col2.metric("Mean coherence", f"{summary['mean_coherence']:.4f}" if summary["mean_coherence"] is not None else "-")
        col3.metric("Max |cumsum|", f"{summary['max_abs_cumsum']:.2f}" if summary["max_abs_cumsum"] is not None else "-")
        col4.metric(
            "Avg active devices",
            f"{summary['active_devices_mean']:.1f}" if summary["active_devices_mean"] is not None else "-",
        )


def build_uploaded_datasets(uploaded_files) -> tuple[list[ParsedDataset], list[str]]:
    datasets: list[ParsedDataset] = []
    errors: list[str] = []
    for uploaded in uploaded_files:
        try:
            datasets.append(parse_uploaded_file(uploaded.getvalue(), uploaded.name))
        except Exception as exc:
            errors.append(f"{uploaded.name}: {exc}")
    return datasets, errors


def main() -> None:
    st.title("GCP2 Data Analysis App")
    st.caption(
        "Upload GCP 2.0 Device Coherence or Network Coherence CSV files, "
        "filter by time window, compare datasets, and export charts."
    )
    st.info(
        "This app is designed for public sharing: users open the link, upload their own CSV files, "
        "and run the analysis directly in the browser."
    )

    with st.expander("How To Use This App", expanded=False):
        guide_tab, device_tab, network_tab, privacy_tab = st.tabs(
            ["Quick Start", "Device Data", "Network Data", "Public App Notes"]
        )
        with guide_tab:
            st.markdown(
                """
                1. Upload one or more GCP2 CSV or ZIP files
                2. Choose your display timezone and date/time filters
                3. Review the detected dataset type and date coverage
                4. Explore the charts and breakdown tabs
                5. Export PNG or filtered CSV when needed
                6. Save analysis metadata for future reference
                """
            )
        with device_tab:
            st.markdown(
                """
                Device files should include:
                - `device_number`
                - `epoch_time_utc`
                - `active_seconds`
                - `device_coherence`
                - `significance`

                The app will:
                - recognize the device ID
                - chart device coherence over time
                - show significance breakdowns
                - flag reduced coverage when `active_seconds` is below `3600`
                """
            )
        with network_tab:
            st.markdown(
                """
                Network files should include:
                - `epoch_time_utc`
                - `network_coherence`
                - `active_devices`

                The app will:
                - plot raw network coherence
                - plot cumulative network coherence
                - show an envelope view based on the current implementation
                - summarize positive and negative coherence values
                """
            )
        with privacy_tab:
            st.markdown(
                """
                This app is intended to be publicly accessible by link.

                Important:
                - the GitHub repository holds the source code
                - the deployed Streamlit URL is the app your users will open
                - anyone with the deployed app link can use it if the deployment is public
                - uploaded data should be treated carefully before public deployment
                """
            )
    use_demo_data = st.toggle("Use bundled demo data", value=False)

    uploaded_files = st.file_uploader(
        "Upload one or more GCP2 CSV files",
        type=["csv", "zip"],
        accept_multiple_files=True,
    )

    datasets: list[ParsedDataset] = []
    errors: list[str] = []
    if use_demo_data:
        datasets.extend(load_demo_datasets())
    if uploaded_files:
        uploaded_datasets, upload_errors = build_uploaded_datasets(uploaded_files)
        datasets.extend(uploaded_datasets)
        errors.extend(upload_errors)

    if not datasets:
        st.info("Upload at least one GCP2 CSV or ZIP file to begin.")
        return

    for error in errors:
        st.error(error)

    with st.expander("Detected files", expanded=True):
        for dataset in datasets:
            st.subheader(dataset.file_name)
            render_dataset_overview(dataset)

    all_dates = pd.concat([dataset.dataframe["datetime_utc"] for dataset in datasets])
    min_date = all_dates.min().date()
    max_date = all_dates.max().date()

    st.sidebar.header("Analysis Controls")
    analysis_mode = st.sidebar.radio(
        "Analysis mode",
        options=["All uploaded data", "Device only", "Network only"],
        index=0,
    )
    timezone_name = st.sidebar.selectbox(
        "Display timezone",
        options=[
            "UTC",
            "Asia/Kolkata",
            "America/New_York",
            "America/Los_Angeles",
            "Europe/London",
        ],
        index=0,
    )
    start_date, end_date = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    start_clock = st.sidebar.time_input("Start time", value=time(0, 0))
    end_clock = st.sidebar.time_input("End time", value=time(23, 59))

    st.sidebar.caption("All calculations remain UTC-based. Timezone selection changes display only.")

    filtered_datasets: list[ParsedDataset] = []
    for dataset in datasets:
        filtered = filter_by_date_and_time(
            dataset.dataframe,
            timezone_name=timezone_name,
            start_date=start_date,
            end_date=end_date,
            start_time=start_clock,
            end_time=end_clock,
        )
        filtered_datasets.append(
            ParsedDataset(
                file_name=dataset.file_name,
                data_type=dataset.data_type,
                dataframe=filtered,
                source_label=dataset.source_label,
                device_id=dataset.device_id,
                group_name=dataset.group_name,
            )
        )

    device_sets = [dataset for dataset in filtered_datasets if dataset.data_type == "device"]
    network_sets = [dataset for dataset in filtered_datasets if dataset.data_type == "network"]

    if analysis_mode == "Device only":
        network_sets = []
    elif analysis_mode == "Network only":
        device_sets = []

    selected_device_labels = []
    if len(device_sets) > 1:
        selected_device_labels = st.sidebar.multiselect(
            "Devices to compare",
            options=[dataset_option_label(dataset) for dataset in device_sets],
            default=[dataset_option_label(dataset) for dataset in device_sets[:4]],
        )
        selected_map = {dataset_option_label(dataset): dataset for dataset in device_sets}
        device_sets = [selected_map[label] for label in selected_device_labels][:4]
    else:
        device_sets = device_sets[:4]

    selected_network_labels = []
    if len(network_sets) > 1:
        selected_network_labels = st.sidebar.multiselect(
            "Network datasets to show",
            options=[dataset_option_label(dataset) for dataset in network_sets],
            default=[dataset_option_label(dataset) for dataset in network_sets],
        )
        selected_map = {dataset_option_label(dataset): dataset for dataset in network_sets}
        network_sets = [selected_map[label] for label in selected_network_labels]

    overview_col1, overview_col2, overview_col3 = st.columns(3)
    overview_col1.metric("Uploaded files", len(datasets))
    overview_col2.metric("Device datasets", len([d for d in filtered_datasets if d.data_type == "device"]))
    overview_col3.metric("Network datasets", len([d for d in filtered_datasets if d.data_type == "network"]))

    with st.expander("Current Analysis Window", expanded=False):
        st.write(f"Display timezone: `{timezone_name}`")
        st.write(f"Date range: `{start_date}` to `{end_date}`")
        st.write(f"Time range: `{start_clock.isoformat()}` to `{end_clock.isoformat()}`")
        st.write(f"Analysis mode: `{analysis_mode}`")

    if device_sets:
        st.header("Device Coherence")
        for dataset in device_sets:
            st.subheader(dataset.source_label)
            show_quality_issues(dataset)
            summary = device_summary(dataset.dataframe)
            render_summary_metrics(dataset.source_label, summary, "device")
            st.write(build_device_summary_text(dataset.source_label, summary))
            detail_tab, breakdown_tab, export_tab = st.tabs(["Chart", "Breakdown", "Export"])
            with detail_tab:
                fig = device_line_figure(dataset.dataframe, f"{dataset.source_label} Device Coherence")
                st.plotly_chart(fig, use_container_width=True)
            with breakdown_tab:
                breakdown = significance_breakdown(dataset.dataframe)
                st.dataframe(breakdown, use_container_width=True, hide_index=True)
            with export_tab:
                export_col1, export_col2 = st.columns(2)
                export_col1.download_button(
                    "Download filtered CSV",
                    dataset.dataframe.to_csv(index=False).encode("utf-8"),
                    file_name=f"{dataset.source_label.replace(' ', '_').lower()}_filtered.csv",
                    mime="text/csv",
                )
                image_bytes = figure_download_bytes(fig)
                if image_bytes:
                    export_col2.download_button(
                        "Download PNG",
                        image_bytes,
                        file_name=f"{dataset.source_label.replace(' ', '_').lower()}.png",
                        mime="image/png",
                    )

        if len(device_sets) > 1:
            comparison = [(dataset.source_label, dataset.dataframe) for dataset in device_sets]
            st.subheader("Multi-Device Comparison")
            compare_fig = multi_device_figure(comparison)
            st.plotly_chart(compare_fig, use_container_width=True)

    if network_sets:
        st.header("Network Coherence")
        for dataset in network_sets:
            st.subheader(dataset.source_label)
            show_quality_issues(dataset)
            summary = network_summary(dataset.dataframe)
            breakdown = network_breakdown(dataset.dataframe)
            render_summary_metrics(dataset.source_label, summary, "network")
            st.write(build_network_summary_text(dataset.source_label, summary))
            detail_tab, stats_tab, export_tab = st.tabs(["Charts", "Breakdown", "Export"])
            with detail_tab:
                raw_fig = raw_network_figure(dataset.dataframe, f"{dataset.source_label} Raw Network Coherence")
                cumsum_fig = network_cumsum_figure(
                    dataset.dataframe,
                    f"{dataset.source_label} Cumulative Network Coherence",
                )
                st.plotly_chart(raw_fig, use_container_width=True)
                st.plotly_chart(cumsum_fig, use_container_width=True)
            with stats_tab:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Positive rows", f"{breakdown['positive_rows']:,}")
                col2.metric("Negative rows", f"{breakdown['negative_rows']:,}")
                col3.metric(
                    "Largest positive",
                    f"{breakdown['largest_positive']:.4f}" if breakdown["largest_positive"] is not None else "-",
                )
                col4.metric(
                    "Largest negative",
                    f"{breakdown['largest_negative']:.4f}" if breakdown["largest_negative"] is not None else "-",
                )
            with export_tab:
                export_col1, export_col2 = st.columns(2)
                export_col1.download_button(
                    "Download filtered CSV",
                    dataset.dataframe.to_csv(index=False).encode("utf-8"),
                    file_name=f"{dataset.source_label.replace(' ', '_').lower()}_filtered.csv",
                    mime="text/csv",
                    key=f"{dataset.file_name}_csv",
                )
                image_bytes = figure_download_bytes(cumsum_fig)
                if image_bytes:
                    export_col2.download_button(
                        "Download PNG",
                        image_bytes,
                        file_name=f"{dataset.source_label.replace(' ', '_').lower()}_cumsum.png",
                        mime="image/png",
                        key=f"{dataset.file_name}_png",
                    )

    st.header("Save Analysis")
    with st.form("save-analysis"):
        title = st.text_input("Analysis title")
        event_name = st.text_input("Event or study name")
        event_context = st.text_input("Context or location")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save analysis metadata")
        if submitted:
            payload = {
                "title": title,
                "event_name": event_name,
                "event_context": event_context,
                "notes": notes,
                "timezone": timezone_name,
                "analysis_mode": analysis_mode,
                "date_range": [str(start_date), str(end_date)],
                "time_range": [start_clock.isoformat(), end_clock.isoformat()],
                "datasets": [
                    {
                        "file_name": dataset.file_name,
                        "type": dataset.data_type,
                        "source_label": dataset.source_label,
                        "rows_after_filter": int(len(dataset.dataframe)),
                        "quality_issues": detect_quality_issues(dataset.dataframe, dataset.data_type),
                    }
                    for dataset in filtered_datasets
                ],
            }
            target = save_analysis_record(ANALYSIS_DIR, payload)
            st.success(f"Saved analysis metadata to {target}")

    st.divider()
    st.caption(
        "Public deployment target: GitHub repository + Streamlit Community Cloud. "
        "Users will open the deployed app link, not the GitHub code link."
    )


if __name__ == "__main__":
    main()
