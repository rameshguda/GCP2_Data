# GCP2 Data Analysis App Project Plan

## Project Goal

Build a public Streamlit application that allows users to upload GCP 2.0 CSV downloads, analyze Device Coherence and Network Coherence data, visualize the results in charts similar to the GCP 2.0 website and community examples, export results, and save analysis details for future reference.

The application should be simple enough for citizen scientists to use, while still being reliable enough for serious exploratory analysis.

## Project Context

Global Consciousness Project 2.0 (GCP 2.0) collects RNG data from physical devices hosted by citizen scientists. Users can download:

- Device Coherence data for individual devices
- Network Coherence data for the global network or specific clusters/groups

The app in this repository will not replace GCP 2.0. It will act as an independent analysis and visualization tool for downloaded CSV files.

## Reference Materials

### Local project resources

- [`resources/quick_start_guide.pdf`](/Users/heartmath/Documents/GCP2_Data/resources/quick_start_guide.pdf)
- [`resources/user_manual.pdf`](/Users/heartmath/Documents/GCP2_Data/resources/user_manual.pdf)
- [`resources/data_download_calculations.pdf`](/Users/heartmath/Documents/GCP2_Data/resources/data_download_calculations.pdf)
- [`resources/GCP2_Device_Coherence_Device_337_Latest.csv`](/Users/heartmath/Documents/GCP2_Data/resources/GCP2_Device_Coherence_Device_337_Latest.csv)

### External references

- [GCP2 Data Download](https://gcp2.net/data-results/data-download)
- [GCP2 Event Analysis](https://gcp2.net/data-results/event-analysis)
- [GCP2 How We Do It](https://gcp2.net/rng-network/how-we-do-it)
- [GCP2 playbox reference code](https://github.com/vfp2/gcp2-playbox/tree/main/experiments/1-basic-cumsum-plot)
- [Forum: coherence algorithm](https://forum.mindmatterinteraction.net/t/gcp-2-0-coherence-algorithm/242)
- [Forum: experiment portal update](https://forum.mindmatterinteraction.net/t/global-consciousness-project-experiment-portal-update-integration-with-gcp2-net-data/451/3)
- [GCP Experiments Portal](https://gcp.fp2.dev/)
- [GCP RNG Statistical Analysis Explorer](https://gcpeggs.fp2.dev/)

## Confirmed Data Understanding

### Device Coherence CSV

Observed schema from the local sample:

- `device_number`
- `epoch_time_utc`
- `active_seconds`
- `device_coherence`
- `significance`

Notes:

- `epoch_time_utc` is a Unix timestamp in UTC.
- `device_coherence` is already a smoothed 1-hour metric.
- `active_seconds` may be less than `3600` if there were outages or interruptions.
- `significance` is a categorical label such as `Normal`, `Elevated`, `High`, `Very High`, or `Extreme`.

### Network Coherence CSV

Documented schema from the calculation PDF:

- `epoch_time_utc`
- `network_coherence`
- `active_devices`

Notes:

- `epoch_time_utc` is a Unix timestamp in UTC.
- The key event plot is produced by taking a cumulative sum of `network_coherence`.
- The blue envelope is based on a 95% confidence interval with increasing degrees of freedom over time.

## Product Vision

The app should let a user:

1. Upload one or more GCP 2.0 CSV files
2. Automatically identify the file type and relevant metadata
3. Select a date range and optional time range
4. Generate useful charts and summary metrics
5. Compare multiple devices in the same view
6. Export charts and filtered data
7. Save an analysis session with event details and notes

## Core User Stories

### Device analysis

- As a device host, I want to upload my device CSV and view coherence over a selected period
- As a researcher, I want to compare up to 4 device files over the same time window
- As a user, I want to see significance levels and identify periods of elevated coherence

### Network analysis

- As a researcher, I want to upload network coherence data and generate cumulative-sum event plots
- As a user, I want to inspect a selected event window and see whether the data departs from expectation
- As a user, I want to export plot data and chart images

### Workflow and reporting

- As a user, I want the app to detect device IDs automatically where possible
- As a user, I want to save an event title, notes, and date/time details with my analysis
- As a user, I want the app to generate a short summary of what the selected data shows

## Proposed V1 Scope

### Included in V1

- Streamlit-based public web app
- CSV upload for Device Coherence and Network Coherence
- Automatic file-type detection
- Date range filter
- Optional time-of-day filter
- UTC as the internal reference timezone
- User-selectable display timezone
- Single-device analysis charts
- Multi-device comparison charts for up to 4 devices
- Network cumulative-sum plot
- Network envelope plot
- Export filtered data to CSV
- Export charts to PNG
- Save analysis metadata locally
- Basic descriptive summaries

### Excluded from V1

- Direct integration with GCP2 user accounts
- Automatic download from GCP2.net
- Realtime data syncing
- Multi-user authentication
- Full scientific report generation
- Advanced ML or AI-driven inference about causation

## Functional Requirements

### File ingestion

- Users can upload one or more CSV files
- The app detects whether a file is:
  - Device Coherence
  - Network Coherence
- The app validates required columns
- The app shows clear errors for invalid or unsupported files

### Metadata extraction

- Extract device number from device files
- Derive file coverage:
  - minimum datetime
  - maximum datetime
  - row count
- Prompt the user for missing metadata if not present in file content

### Filtering

- Filter by date range
- Filter by optional time-of-day range
- Handle timezone display without changing UTC-based calculations
- Warn when gaps or malformed rows are detected

### Device analysis

- Plot device coherence over time
- Highlight significance levels
- Compare up to 4 uploaded devices
- Show summary metrics:
  - max coherence
  - mean coherence
  - number of elevated periods
  - coverage completeness based on `active_seconds`

### Network analysis

- Plot raw network coherence over time
- Plot cumulative sum of network coherence
- Plot confidence envelope around the cumulative series
- Show event-window stats
- Support group-level analysis if metadata is available

### Export and persistence

- Download chart as PNG
- Download filtered data as CSV
- Save analysis metadata:
  - event title
  - notes
  - selected files
  - selected range
  - selected timezone

### Summaries

- Provide a plain-language summary of selected data
- Describe peaks, dips, and periods of elevated significance
- Clearly distinguish descriptive summaries from scientific conclusions

## Non-Functional Requirements

- Easy for non-technical users
- Works well in desktop browsers
- Acceptable usability on mobile for viewing
- Reproducible UTC-based calculations
- Clear validation and error messaging
- Maintainable Python codebase
- Public deployment from GitHub

## Recommended Technical Architecture

### Stack

- Frontend + app framework: Streamlit
- Data processing: pandas, numpy
- Plotting: Plotly
- Statistical utilities: scipy
- Persistence for saved analyses: JSON files or SQLite
- Testing: pytest

### App modules

- `app.py`
  - Streamlit entrypoint
- `src/parsers.py`
  - CSV detection and validation
- `src/time_utils.py`
  - epoch conversion, timezone handling, filtering
- `src/device_analysis.py`
  - device-specific metrics and chart preparation
- `src/network_analysis.py`
  - cumsum and envelope calculations
- `src/plots.py`
  - shared plotting helpers
- `src/storage.py`
  - save and load analysis metadata
- `src/summaries.py`
  - descriptive narrative summaries
- `tests/`
  - parsing, calculations, and edge-case tests

## Data Flow

1. User uploads one or more CSV files
2. App inspects schema and classifies file type
3. App parses timestamps and normalizes all analysis to UTC
4. App extracts metadata and presents filter controls
5. User selects date/time window and analysis mode
6. Analysis engine computes filtered metrics and plot data
7. Visualization layer renders charts
8. User exports PNG/CSV or saves the analysis session

## Milestones

### Milestone 1: Discovery and specification

- Confirm all supported file schemas
- Collect at least one real Network Coherence CSV
- Confirm desired chart types for V1
- Decide how saved analyses should be stored

Deliverable:

- finalized project scope and data contract

### Milestone 2: Project scaffold

- Initialize Python project structure
- Add Streamlit app shell
- Add dependencies and local run instructions
- Add sample data folder conventions

Deliverable:

- runnable Streamlit shell committed to repo

### Milestone 3: CSV parsing and validation

- Implement file detection
- Validate columns and types
- Parse UTC timestamps
- Build date range extraction

Deliverable:

- upload and file inspection workflow

### Milestone 4: Device analysis

- Single-device chart
- Multi-device comparison
- Significance display
- Summary metrics

Deliverable:

- working device analysis section

### Milestone 5: Network analysis

- Raw network chart
- Cumulative-sum chart
- Confidence envelope
- Event-window stats

Deliverable:

- working network analysis section

### Milestone 6: Export and saved analyses

- PNG export
- CSV export
- Save analysis metadata and notes

Deliverable:

- usable reporting workflow

### Milestone 7: Validation and deployment

- Compare outputs against known GCP2 examples
- Add tests for parsing and calculations
- Deploy public app
- Write user documentation

Deliverable:

- public V1 deployment

## Key Risks and Roadblocks

### 1. Missing network sample file

Current status:

- A local Device Coherence sample exists
- A local Network Coherence sample was not found in the `resources` folder during initial review

Impact:

- We can define the parser from documentation
- We cannot validate the full network plotting workflow with confidence until we test against a real file

Mitigation:

- Add one or more real network CSV samples to `resources`
- Use these samples to validate cumsum and envelope behavior

### 2. Exact chart replication may require iteration

Impact:

- The high-level network plot recipe is clear
- The exact display conventions on GCP2 may include smoothing, exclusions, scales, or styling details not fully documented

Mitigation:

- Treat V1 as scientifically consistent and visually similar
- Compare outputs with GCP2 examples and refine

### 3. Timezone confusion

Impact:

- Users will often reason in local time
- Source data is in UTC

Mitigation:

- Keep UTC internal
- Let users choose a display timezone
- Make timezone labeling explicit everywhere

### 4. Data gaps and malformed input

Impact:

- Missing/bad dates are acknowledged by GCP2 itself
- Some files may contain gaps or reduced coverage

Mitigation:

- Add validation and warnings
- Mark incomplete intervals
- Avoid silently dropping problematic rows

### 5. Scope creep

Impact:

- The request includes uploading, analysis, exports, saved sessions, and summaries
- It can easily expand into a full research platform

Mitigation:

- Keep V1 focused on CSV-based analysis and export
- Defer automation, live APIs, and advanced collaboration features

## Assumptions

- The app is intended for public use by link, not private authenticated use
- Users will upload data they already downloaded from GCP2.net
- V1 does not need direct integration with GCP2 accounts
- Device comparison will initially be limited to about 4 devices
- Summary generation will initially be descriptive rather than interpretive

## Validation Strategy

- Use the local device sample to verify parsing and charts
- Add one or more network CSV samples to verify cumsum and envelope calculations
- Compare network plots against:
  - GCP2 event examples
  - community reference implementations
- Add automated tests for:
  - timestamp conversion
  - file detection
  - filtering
  - cumulative sum calculations
  - confidence envelope output shape and stability

## Immediate Next Steps

1. Add a sample Network Coherence CSV into `resources`
2. Confirm the exact chart types desired for V1
3. Scaffold the Streamlit project structure
4. Implement CSV parsing and upload validation
5. Build device and network chart prototypes

## Suggested V1 Success Criteria

V1 can be considered successful when:

- a user can upload valid device and network CSV files
- the app detects the file type correctly
- the app filters by date/time reliably
- the app produces device and network charts without manual preprocessing
- the app exports PNG and CSV successfully
- the app saves analysis metadata and notes
- the resulting plots are close enough to trusted GCP2 references for practical research use

## Open Questions

- What exact chart set should V1 include for Device Coherence?
- Should saved analyses be local-only or shared across users?
- Should summaries be purely statistical or include optional AI-generated narrative?
- Which deployment target should be preferred:
  - Streamlit Community Cloud
  - Hugging Face Spaces
  - VPS or custom hosting
- Do we want to support direct import of files from cloud storage later?

## Conclusion

This project is viable and has a clear path forward. The best approach is to start with a focused Streamlit V1 built around uploaded CSV files, strong parsing, reliable UTC-based filtering, device and network analysis, and export features. The main near-term blocker is validating the Network Coherence workflow with a real sample file.
