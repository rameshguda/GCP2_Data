# GCP2 Consciousness Data Analyzer -- Complete App Development Prompt & Technical Specification

**Version:** 2.0
**Date:** 2026-04-11
**Author:** Ramesh Guda, HeartMath Citizen Scientist
**Status:** Canonical Reference Document

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Vision & Goals](#2-project-vision--goals)
3. [Target Users & Personas](#3-target-users--personas)
4. [Application Architecture](#4-application-architecture)
5. [Data Schema & Ingestion Specifications](#5-data-schema--ingestion-specifications)
6. [Mathematical & Statistical Foundations](#6-mathematical--statistical-foundations)
7. [Chart Plotting Technical Specifications (Single Source of Truth)](#7-chart-plotting-technical-specifications-single-source-of-truth)
8. [Device Naming & Configuration System](#8-device-naming--configuration-system)
9. [Analysis Engine & Report Generation](#9-analysis-engine--report-generation)
10. [User Interface & Experience Design](#10-user-interface--experience-design)
11. [Multi-File Upload & Data Management](#11-multi-file-upload--data-management)
12. [Export & Download System](#12-export--download-system)
13. [Deployment & GitHub Repository](#13-deployment--github-repository)
14. [Project Plan & Milestones](#14-project-plan--milestones)
15. [Testing & Validation Strategy](#15-testing--validation-strategy)
16. [Reference Materials & External Sources](#16-reference-materials--external-sources)
17. [Appendices](#17-appendices)

---

## 1. Executive Summary

### What This App Is

The **GCP2 Consciousness Data Analyzer** is a free, publicly accessible web application hosted on GitHub that enables citizen scientists, researchers, and consciousness-curious individuals to deeply analyze Random Number Generator (RNG) data from the Global Consciousness Project 2.0 (GCP 2.0). The app accepts CSV files downloaded directly from [gcp2.net](https://gcp2.net) and transforms raw quantum noise data into readable, scientifically rigorous visualizations and reports that tell the story of human consciousness.

### What Problem It Solves

GCP 2.0 provides raw data downloads, but citizen scientists currently lack an accessible, dedicated tool to:

- Perform deep analysis on their own hosted devices (typically 4-5 devices)
- Compare Device Coherence and Network Coherence side by side
- Generate publication-quality charts that exactly match GCP2.net Event Analysis formatting
- Produce structured analytical reports pinpointing when devices entered significant states
- Correlate local device activity with global network consciousness events

### Core Principle

Every chart, calculation, and visualization produced by this app must be **mathematically faithful** to the GCP 2.0 scientific methodology as documented in the official data_download_calculations.pdf, the Bancel and Nelson (2008) Journal of Scientific Exploration paper, and the reference implementations at [github.com/vfp2/gcp2-playbox](https://github.com/vfp2/gcp2-playbox).

---

## 2. Project Vision & Goals

### Primary Goals

1. **Accessible Analysis** -- Anyone with the app link can access it; no login or account required
2. **Scientific Accuracy** -- All charts and calculations match GCP2.net methodology exactly
3. **Device-Focused Research** -- Designed for analyzing 4-5 RNG devices in depth
4. **Dual Data Support** -- Accept and analyze both Device Coherence and Network Coherence CSV files
5. **Comparative Analysis** -- Enable cross-comparison between device activity and network coherence
6. **Report Generation** -- Produce structured, downloadable reports with key findings
7. **Chart Fidelity** -- Charts visually and mathematically replicate GCP2.net Event Analysis plots

### Secondary Goals

8. **Device Personalization** -- Allow users to name devices with meaningful labels
9. **Export Everything** -- Charts as PNG/PDF, reports as PNG/PDF, filtered data as CSV
10. **Event Correlation** -- Identify periods where both Device and Network Coherence show simultaneous significance
11. **Citizen Science Empowerment** -- Help non-technical users understand what their RNG data reveals about consciousness fields

### Non-Goals (Explicitly Out of Scope)

- Real-time live data streaming from GCP2.net
- Direct integration with GCP2 user accounts or APIs
- Multi-user authentication or collaborative workspaces
- Machine learning inference about causation
- Replacement of gcp2.net -- this is a complementary analysis tool

---

## 3. Target Users & Personas

### Persona 1: Device Host (Primary)

- **Profile:** Citizen scientist who hosts 1-5 NextGen RNG devices
- **Technical Level:** Non-programmer, comfortable with web apps and spreadsheets
- **Goal:** Understand when their device(s) showed unusual coherence, correlate with local events/meditations
- **Example:** Ramesh hosts Device 15 (Lab1) and Device 337 (Control) in India, and wants to analyze data around meditation events

### Persona 2: Event Researcher

- **Profile:** Organizer of group meditations, retreats, or consciousness experiments
- **Technical Level:** Moderate; can follow instructions, interpret charts
- **Goal:** Download Network Coherence data for a specific event window, generate a chart showing if the red curve exited the blue envelope, produce a report for participants
- **Example:** A HeartMath facilitator running a Global Coherence meditation wants to show participants the network's response during their session

### Persona 3: Citizen Analyst

- **Profile:** GCP2 community member interested in exploring historical data patterns
- **Technical Level:** Varies; some are programmers, others are not
- **Goal:** Compare multiple devices, look for cross-correlations, download publication-quality charts
- **Example:** A forum member wants to compare 4 city-cluster devices during a major global event

---

## 4. Application Architecture

### 4.1 Framework Recommendation

**Primary Recommendation: Streamlit**

After evaluating multiple Python-based open-source frameworks, **Streamlit** remains the optimal choice for this project for the following reasons:

| Criterion | Streamlit | Dash (Plotly) | Panel (HoloViz) | Gradio | Reflex |
|-----------|-----------|---------------|------------------|--------|--------|
| Ease of development | Excellent | Good | Good | Excellent | Good |
| Chart interactivity | Excellent (Plotly) | Excellent | Good | Limited | Good |
| Free cloud hosting | Streamlit Cloud | Render/Heroku | Heroku | HuggingFace | Reflex Cloud |
| GitHub integration | Native | Manual | Manual | HuggingFace | Manual |
| Citizen scientist UX | Excellent | Complex | Complex | Too simple | Good |
| PDF/PNG export | kaleido | kaleido | selenium | Limited | Manual |
| Multi-file upload | Native | More code | More code | Native | More code |
| Session state | Built-in | Flask-based | Param-based | Limited | Built-in |
| Community adoption | Largest | Large | Small | Growing | Small |

**Why Not Dash?** -- While Dash offers deeper callback control, the added complexity of managing callbacks vs. Streamlit's linear script model is unnecessary for this app's scope. Dash's learning curve would slow iteration without providing proportional benefit.

**Why Not Gradio?** -- Gradio excels at ML model demos but lacks the layout flexibility and session state management needed for multi-file analytical workflows.

**Verdict:** Stay with Streamlit. It provides the best balance of rapid development, free hosting, GitHub integration, and citizen-scientist-friendly UX.

### 4.2 Technology Stack

```
Frontend/App Framework:  Streamlit >= 1.44
Data Processing:         pandas >= 2.2, numpy >= 1.26
Visualization:           Plotly >= 5.24
Statistical Engine:      scipy >= 1.13 (chi2 distribution)
Image Export:            kaleido >= 0.2.1 (PNG/PDF from Plotly)
PDF Report Generation:   fpdf2 >= 2.8 (or reportlab)
Testing:                 pytest >= 8
Version Control:         Git + GitHub
Deployment:              Streamlit Community Cloud (free)
```

### 4.3 Module Architecture

```
gcp2-analyzer/
|
+-- app.py                          # Streamlit entry point
+-- requirements.txt                # Python dependencies
+-- .streamlit/
|   +-- config.toml                 # Theme configuration
|
+-- src/
|   +-- __init__.py
|   +-- parsers.py                  # CSV detection, validation, normalization
|   +-- time_utils.py               # UTC handling, timezone conversion, filtering
|   +-- device_analysis.py          # Device metrics, significance classification
|   +-- network_analysis.py         # Cumsum, envelope, network metrics
|   +-- correlation_analysis.py     # NEW: Device-Network correlation engine
|   +-- plots.py                    # All chart generation (Plotly)
|   +-- reports.py                  # NEW: Structured report generation
|   +-- summaries.py                # Plain-text narrative summaries
|   +-- quality.py                  # Data quality checks and warnings
|   +-- storage.py                  # Analysis persistence (JSON)
|   +-- device_config.py            # NEW: Device naming/aliasing system
|   +-- demo_data.py                # Bundled sample datasets
|   +-- constants.py                # NEW: All thresholds, colors, and constants
|
+-- tests/
|   +-- test_parsers.py
|   +-- test_analysis.py
|   +-- test_network_math.py        # NEW: Envelope and cumsum validation
|   +-- test_correlation.py         # NEW: Correlation logic tests
|   +-- test_charts.py              # NEW: Chart output validation
|
+-- resources/
|   +-- sample CSV files
|   +-- reference images for chart validation
|
+-- saved_analyses/                 # User-saved analysis sessions (JSON)
+-- device_config.json              # Persisted device names
+-- README.md
+-- PROJECT_PLAN.md
+-- DEPLOYMENT.md
```

### 4.4 Data Flow Architecture

```
                         +------------------+
                         |   User Browser   |
                         +--------+---------+
                                  |
                    Upload CSV(s) | Select Date/Time
                                  v
                         +------------------+
                         |  Streamlit App   |
                         |    (app.py)      |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
          +-----------------+        +--------------------+
          |  parsers.py     |        |  device_config.py  |
          |  Detect type    |        |  Load/save names   |
          |  Validate cols  |        +--------------------+
          |  Normalize data |
          +--------+--------+
                   |
         +---------+-----------+
         |                     |
         v                     v
  +----------------+   +------------------+
  | Device Branch  |   | Network Branch   |
  | device_        |   | network_         |
  | analysis.py    |   | analysis.py      |
  +-------+--------+   +--------+---------+
          |                      |
          +----------+-----------+
                     |
                     v  (if both uploaded)
          +---------------------+
          | correlation_        |
          | analysis.py         |
          | Compare Device vs   |
          | Network Coherence   |
          +----------+----------+
                     |
          +----------+----------+
          |                     |
          v                     v
   +-------------+      +-------------+
   |  plots.py   |      | reports.py  |
   |  Generate   |      | Generate    |
   |  charts     |      | analysis    |
   +------+------+      | reports     |
          |              +------+------+
          v                     v
   +-------------+      +-------------+
   | PNG / PDF   |      | PNG / PDF   |
   | chart       |      | report      |
   | download    |      | download    |
   +-------------+      +-------------+
```

---

## 5. Data Schema & Ingestion Specifications

### 5.1 Device Coherence CSV

**Source:** Downloaded from gcp2.net > Data & Results > Data Download > Device Coherence

**Schema:**

| Column | Type | Description |
|--------|------|-------------|
| `device_number` | integer | Unique ID for the RNG device (matches globe/map on gcp2.net) |
| `epoch_time_utc` | integer | Unix timestamp in UTC; the second this coherence was calculated |
| `active_seconds` | integer | Seconds of data uploaded in the preceding hour (max 3600) |
| `device_coherence` | float | Smoothed 1-hour Device Coherence value |
| `significance` | string | Categorical: Normal, Elevated, High, Very High, Extreme |

**Sample Row:**
```csv
device_number,epoch_time_utc,active_seconds,device_coherence,significance
337,1775001659,3600,99.2027,Normal
```

**Critical Notes:**
- Data arrives at approximately **60-second intervals** (one row per minute)
- `device_coherence` is **already smoothed**: it is the absolute value of the 1-hour moving sum of raw Device Coherence (see Section 6)
- `active_seconds < 3600` indicates an incomplete hour (outage, startup, etc.)
- The device has **4 RNGs internally**; coherence is measured across **3 of 4** (the 4th is sequestered for future research)

### 5.2 Network Coherence CSV

**Source:** Downloaded from gcp2.net > Data & Results > Data Download > Network Coherence

**Schema:**

| Column | Type | Description |
|--------|------|-------------|
| `epoch_time_utc` | integer | Unix timestamp in UTC; the second this coherence was calculated |
| `network_coherence` | float | Network Coherence value for this group at this second |
| `active_devices` | integer | Number of devices contributing to this calculation |

**Sample Row:**
```csv
epoch_time_utc,network_coherence,active_devices
1756684800,-0.869,353
```

**Critical Notes:**
- Data arrives at **1-second granularity** (one row per second)
- Network Coherence can be **positive or negative** (unlike smoothed Device Coherence which is always positive due to absolute value)
- `active_devices` fluctuates as devices join/leave the network
- Each device contributes 4 RNGs, so 353 devices = 1,412 RNGs
- Data can be downloaded for: Global Network, City Clusters, or Custom Groups
- The filename typically encodes the group: e.g., `GCP2_Network_Coherence_Global_Network_2026_03.csv`

### 5.3 File Detection Logic

The app must auto-detect file type by inspecting column headers:

```python
DEVICE_REQUIRED_COLUMNS = {"device_number", "epoch_time_utc", "active_seconds",
                           "device_coherence", "significance"}

NETWORK_REQUIRED_COLUMNS = {"epoch_time_utc", "network_coherence", "active_devices"}

def detect_dataset_type(df: pd.DataFrame) -> str:
    columns = set(col.strip().lower() for col in df.columns)
    if DEVICE_REQUIRED_COLUMNS.issubset(columns):
        return "device"
    elif NETWORK_REQUIRED_COLUMNS.issubset(columns):
        return "network"
    else:
        return "unknown"
```

### 5.4 File Ingestion Pipeline

```
Raw Upload (CSV or ZIP)
    |
    v
Extract CSV (if ZIP, extract first .csv file)
    |
    v
Read CSV with pandas (handle encoding, whitespace in headers)
    |
    v
Normalize column names (strip, lowercase)
    |
    v
Detect dataset type (device vs. network)
    |
    v
Type-coerce columns (int for epoch, float for coherence, etc.)
    |
    v
Convert epoch_time_utc -> datetime_utc (UTC datetime object)
    |
    v
Sort by datetime_utc ascending
    |
    v
Extract metadata:
  - Device: device_number from data column + filename
  - Network: group name from filename pattern
  - Date range: min/max datetime
  - Row count
    |
    v
Return ParsedDataset(dataframe, type, metadata)
```

### 5.5 Validation Rules

| Check | Device | Network | Action |
|-------|--------|---------|--------|
| Required columns present | Yes | Yes | Reject file with error |
| `epoch_time_utc` is numeric | Yes | Yes | Reject row |
| `device_coherence` is numeric | Yes | -- | Coerce or warn |
| `significance` is valid category | Yes | -- | Warn if unknown value |
| `network_coherence` is numeric | -- | Yes | Coerce or warn |
| `active_seconds` between 0-3600 | Yes | -- | Warn if out of range |
| `active_devices` > 0 | -- | Yes | Warn if zero |
| Duplicate timestamps | Yes | Yes | Warn |
| Gaps in time series | Yes | Yes | Warn with gap details |

---

## 6. Mathematical & Statistical Foundations

This section defines the complete mathematical framework that underpins every calculation and visualization in the app. It must be treated as authoritative.

### 6.1 The RNG Hardware Foundation

Each NextGen RNG device contains **4 independent True Random Number Generators**. Each RNG produces a stream of random bits (1s and 0s) at 1-bit-per-second resolution, functioning as a sophisticated "coin toss." Under normal conditions, these bits are statistically independent -- deviations from the mean cancel out over time.

**Key Hypothesis:** Shared human attention or collective emotion can cause these independent sensors to synchronize, producing correlated bit patterns across the network. This correlation is measured as **coherence**.

### 6.2 Raw Coherence Calculation

The raw coherence for a device or network at any given second is derived from chi-squared (chi2) statistics applied to the bit streams. The mathematical basis follows Bancel and Nelson's Journal of Scientific Exploration 2008 paper, where this metric was originally called "Device Variance" (for devices) or "Network Variance" / "NetVar" (for networks).

**For a single device:** Coherence is computed across 3 of the 4 internal RNGs (the 4th is sequestered for future research).

**For the network:** Network Coherence measures whether multiple devices (and the RNGs within them) produce the same bit at the same second -- i.e., inter-device synchronization.

### 6.3 The One-Hour Moving Sum (Smoothing)

The **Device Coherence** value in downloaded CSV files is NOT raw coherence. It is a **smoothed metric** calculated as follows:

```
smoothed_device_coherence(t) = |SUM(raw_device_coherence(t-3599) ... raw_device_coherence(t))|
```

**In words:** Take the raw Device Coherence values for the preceding 3600 seconds (1 hour), sum them, and take the absolute value.

**Why absolute value?** Because we care about the magnitude of deviation from randomness in either direction. Both "coherence" (syncing up) and "anti-coherence" (extreme independence) are scientifically meaningful departures from chance.

### 6.4 Defining Statistical Significance (The Color Zones)

The significance of a smoothed Device Coherence value is determined by comparing it against a **simulated distribution** of what the 1-hour moving sum of chi-squared random data would produce. This yields p-value thresholds:

| Level | Color | p-value | Threshold Value | Meaning |
|-------|-------|---------|-----------------|---------|
| **Normal** | Magenta `#FF00FF` | p > 0.1 | < 243 | Baseline random behavior |
| **Elevated** | Cyan `#00FFFF` | p < 0.1 | >= 243 | Initial signal emergence |
| **High** | Yellow `#FFFF00` | p < 0.05 | >= 288 | Statistical significance begins |
| **Very High** | Orange `#FFA500` | p < 0.01 | >= 378 | Strong non-random evidence |
| **Extreme** | Gold `#FFD700` | p < 0.001 | >= 483 | Highly significant departure (1 in 1,000 odds) |

**Physical Manifestation:** These same color zones are mirrored on the physical NextGen RNG hardware through its ring of 8 LEDs, alerting onsite hosts to significant shifts in real time.

**Transition Values (exact boundaries):**
- Normal -> Elevated: **243**
- Elevated -> High: **288**
- High -> Very High: **378**
- Very High -> Extreme: **483**

### 6.5 Cumulative Sum (CUMSUM) -- The Red Curve

The **Cumulative Sum** is the primary tool for detecting whether consciousness is influencing the random behavior of the sensors. This produces the **Red Curve** in Event Analysis charts.

**Calculation:**

```python
cumulative_coherence[i] = SUM(network_coherence[0] ... network_coherence[i])
```

Or equivalently:
```python
df["cumulative_coherence"] = df["network_coherence"].cumsum()
```

**Interpretation:**

| Red Curve Behavior | Meaning |
|-------------------|---------|
| **Horizontal / near zero** | Network behaving randomly; deviations canceling out |
| **Persistent upward trend** | Sensors are syncing up (coherence); suggests shared human attention |
| **Persistent downward trend** | Sensors showing more independence than chance (anti-coherence) |
| **Exits top of blue envelope** | Statistically significant coherence (p < 0.05) |
| **Exits bottom of blue envelope** | Statistically significant anti-coherence (p < 0.05) |

### 6.6 The Blue Envelope -- 95% Confidence Interval

The **Blue Envelope** is the statistical boundary that separates random fluctuations from significant signals. It forms the parabolic curves surrounding the Red Curve.

#### Why It Is Parabolic

Because the chart plots a cumulative sum, the potential for random fluctuation **increases with time**. The variance of a random walk grows linearly with the number of steps. To maintain a consistent 95% confidence level while degrees of freedom increase, the boundary must **widen over time**, producing the characteristic parabolic shape.

#### Degrees of Freedom (Dynamic)

The degrees of freedom are NOT static. At any point on the x-axis:

```
degrees_of_freedom(x) = number of seconds elapsed from the start of the analysis window
```

**Examples:**
- At x = 1 second: df = 1
- At x = 60 seconds (1 minute): df = 60
- At x = 600 seconds (10 minutes): df = 600
- At x = 3,600 seconds (1 hour): df = 3,600
- At x = 15,000 seconds: df = 15,000

#### Mathematical Formula

The envelope bounds are calculated using the chi-squared distribution's percent point function (inverse CDF):

```python
from scipy.stats import chi2
import numpy as np

n = np.arange(1, num_seconds + 1)  # degrees of freedom = elapsed seconds

# Upper bound (95% confidence)
envelope_upper = np.sqrt(chi2.ppf(0.95, n))

# Lower bound (mirror for two-sided test)
envelope_lower = -envelope_upper
```

**Detailed breakdown:**

1. `chi2.ppf(0.95, n)` -- Returns the chi-squared value below which 95% of data falls for `n` degrees of freedom
2. `np.sqrt(...)` -- Takes the square root because we are working with cumulative sums (standard deviation scale), not variances
3. The negative mirror creates the lower envelope for detecting anti-coherence

#### Additional Confidence Tiers

While the 95% (p=0.05) Blue Envelope is the default visual guide, the mathematical framework supports deeper significance levels:

| Tier | p-value | Use |
|------|---------|-----|
| Near Significant | p < 0.1 | Early signal detection |
| **Significant (Blue Envelope)** | **p < 0.05** | **Standard benchmark** |
| Very Significant | p < 0.01 | Strong evidence |
| Highly Significant | p < 0.001 | Extreme events (e.g., 9/11, major global meditations) |

### 6.7 Interpreting Downward Trends

The statistical model is **two-sided**. A downward exit from the Blue Envelope is equally meaningful:

- **Upward exit:** Sensors syncing up (coherence) -- often correlated with shared human attention/emotion
- **Downward exit:** Sensors showing extreme independence (anti-coherence) -- more divergence than pure chance would produce

**Historical Examples:**
- "Tibetan Bowls" meditation (2025-10-04): Red Curve trended downward significantly but stayed within envelope
- Another event (2025-10-06): Downward trend approached lower significance boundary, labeled "Near Significant"

### 6.8 Network Coherence vs. Device Coherence: Key Differences

| Aspect | Device Coherence | Network Coherence |
|--------|-----------------|-------------------|
| **Granularity** | ~60-second intervals | 1-second intervals |
| **Pre-processing** | Already smoothed (1-hr moving sum, abs value) | Raw values |
| **Value range** | Always >= 0 (due to abs value) | Can be positive or negative |
| **Primary visualization** | Line chart colored by significance | Cumulative sum (Red Curve) |
| **Statistical test** | Pre-classified into significance levels | Tested against Blue Envelope |
| **Measures** | Intra-device RNG coherence (3 of 4 RNGs) | Inter-device network synchronization |

---

## 7. Chart Plotting Technical Specifications (Single Source of Truth)

**This section is the definitive reference for how every chart in the app must be rendered. All color codes, line styles, axis configurations, and visual components are specified here. No chart implementation should deviate from these specifications.**

### 7.1 Network Coherence Event Analysis Chart (Primary Chart)

This is the flagship chart of the application, replicating the GCP2.net Event Analysis visualization.

#### 7.1.1 Visual Components

```
+-----------------------------------------------------------------------+
|                                                                       |
|   [Event Title]                                                       |
|   Start time: YYYY-MM-DD HH:MM:SS [TZ]                              |
|                                                                       |
|   Y-axis: "Network Coherence (P)"                                    |
|                                                                       |
|        ^                                                              |
|        |          ~~~~~~~~  (Red Curve - cumsum)                     |
|        |       ~~~/                                                   |
|        |     ~~/                                                      |
|        |   --/------------ (Blue Upper Envelope)                     |
|        |  / /                                                         |
|   0 ---+--/---------------------------------------------------->     |
|        |  \ \                                                         |
|        |   --\------------ (Blue Lower Envelope)                     |
|        |                                                              |
|        |     X-axis: "minutes" (relative from event start)           |
|        +-------------------------------------------------------->     |
|        0.0     2.5     5.0     7.5     10.0                          |
|                                                                       |
+-----------------------------------------------------------------------+
```

#### 7.1.2 Color Specifications

| Element | Color | Hex Code | RGB | Line Width |
|---------|-------|----------|-----|------------|
| **Red Curve** (Cumulative Sum) | Red | `#FF0000` | (255, 0, 0) | 1.5 px |
| **Blue Envelope** (Upper & Lower) | Blue | `#0000FF` | (0, 0, 255) | 1.5 px |
| **Zero Baseline** | Black | `#000000` | (0, 0, 0) | 1.0 px |
| **Background** | White | `#FFFFFF` | (255, 255, 255) | -- |
| **Grid Lines** | Light Gray | `#E0E0E0` | (224, 224, 224) | 0.5 px |
| **Vertical Event Marker** | Black | `#000000` | (0, 0, 0) | 1.5 px |

**Critical:** The GCP2.net reference chart uses pure **red** (`#FF0000`) for the cumulative sum and pure **blue** (`#0000FF`) for the envelope. Do NOT use muted or branded alternatives for this chart type.

#### 7.1.3 Axis Specifications

**X-Axis (Horizontal):**
- **Label:** `"minutes"`
- **Unit:** Minutes elapsed from the start of the analysis window
- **Format:** Decimal (e.g., 0.0, 2.5, 5.0, 7.5, 10.0)
- **Calculation:** `(elapsed_seconds) / 60.0`
- **Origin:** 0.0 at the event start time
- **Direction:** Left to right, increasing time
- **Tick interval:** Auto-scaled based on duration; prefer multiples of 2.5 for short events, 5 or 10 for longer

**Y-Axis (Vertical):**
- **Label:** `"Network Coherence (P)"`
- **Unit:** Cumulative coherence units (dimensionless statistical measure)
- **Range:** Auto-scaled to fit both the Red Curve and Blue Envelope, with symmetric padding around zero
- **Zero line:** Always visible as a solid black horizontal line
- **Tick interval:** Auto-scaled; prefer round numbers (-50, 0, 50 or -100, -50, 0, 50, 100)

#### 7.1.4 Title Block

```
Line 1: [Event Name / Title]              Font: Large, bold
Line 2: Start time: YYYY-MM-DD HH:MM:SS [TZ]   Font: Medium, regular
```

**Examples from reference charts:**
```
World Navkar Mantra Day - chanting
Start time: 2025-04-09 08:25:00 IST
```

```
Mahayog Dhyan Kumbh - Meditation 2 (Music)
Start time: 2025-10-05 14:30:00 IST
```

#### 7.1.5 Vertical Event Marker

A solid **black vertical line** at x=0 marks the exact start of the event. This appears as a thin vertical line spanning the full y-axis range at the origin.

#### 7.1.6 Time Axis Synchronization

**Critical Implementation Detail:**

The x-axis shows **relative time** (minutes from event start), NOT absolute timestamps. This is essential for:
- Clean, readable axis labels
- Consistent comparison across events of different durations
- Matching GCP2.net's Event Analysis presentation

```python
# Convert absolute timestamps to relative minutes
df["minutes"] = (df["epoch_time_utc"] - event_start_epoch) / 60.0
```

#### 7.1.7 Resolution and Data Density

- Network Coherence data arrives at **1-second granularity**
- For events up to ~30 minutes (1,800 seconds), plot every data point
- For events 30 minutes to 2 hours, consider light downsampling (every 2-3 seconds) for rendering performance
- For events > 2 hours, downsample to ~5-second intervals while preserving peaks
- **Never downsample** the envelope -- it is a smooth mathematical function and renders efficiently at any resolution

#### 7.1.8 Complete Plotly Implementation Reference

```python
import plotly.graph_objects as go
import numpy as np
from scipy.stats import chi2

def network_event_analysis_chart(
    df: pd.DataFrame,
    event_title: str,
    start_time_display: str,
    timezone_label: str,
) -> go.Figure:
    """
    Generate a GCP2.net-style Event Analysis chart.
    
    df must contain:
      - 'minutes': float, relative minutes from event start
      - 'cumulative_coherence': float, running cumsum of network_coherence
      - 'envelope_upper': float, upper 95% CI bound
      - 'envelope_lower': float, lower 95% CI bound
    """
    fig = go.Figure()
    
    # 1. Red Curve -- Cumulative Coherence
    fig.add_trace(go.Scatter(
        x=df["minutes"],
        y=df["cumulative_coherence"],
        mode="lines",
        name="Cumulative Coherence",
        line=dict(color="#FF0000", width=1.5),
        hovertemplate="Min: %{x:.1f}<br>Coherence: %{y:.2f}<extra></extra>",
    ))
    
    # 2. Blue Envelope -- Upper Bound
    fig.add_trace(go.Scatter(
        x=df["minutes"],
        y=df["envelope_upper"],
        mode="lines",
        name="Envelope (95% CI)",
        line=dict(color="#0000FF", width=1.5),
        hovertemplate="Min: %{x:.1f}<br>Upper: %{y:.2f}<extra></extra>",
    ))
    
    # 3. Blue Envelope -- Lower Bound
    fig.add_trace(go.Scatter(
        x=df["minutes"],
        y=df["envelope_lower"],
        mode="lines",
        name="Envelope (95% CI)",
        line=dict(color="#0000FF", width=1.5),
        showlegend=False,
        hovertemplate="Min: %{x:.1f}<br>Lower: %{y:.2f}<extra></extra>",
    ))
    
    # 4. Zero Baseline
    fig.add_hline(y=0, line_color="#000000", line_width=1.0)
    
    # 5. Vertical Event Start Marker
    fig.add_vline(x=0, line_color="#000000", line_width=1.5)
    
    # 6. Layout
    fig.update_layout(
        title=dict(
            text=f"{event_title}<br><sub>Start time: {start_time_display} {timezone_label}</sub>",
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title="minutes",
            zeroline=True,
            zerolinecolor="#000000",
            zerolinewidth=1,
            gridcolor="#E0E0E0",
            gridwidth=0.5,
        ),
        yaxis=dict(
            title="Network Coherence (P)",
            zeroline=True,
            zerolinecolor="#000000",
            zerolinewidth=1,
            gridcolor="#E0E0E0",
            gridwidth=0.5,
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        height=520,
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
```

#### 7.1.9 Pre-Event Window (Optional)

Some analyses benefit from showing data **before** the event starts (negative minutes on x-axis). This provides a baseline for comparison:

- Include 5-15 minutes of pre-event data when available
- The vertical marker at x=0 clearly delineates "before" vs. "during"
- Pre-event data should show the Red Curve establishing its random baseline near zero

### 7.2 Device Coherence Timeline Chart

#### 7.2.1 Visual Design

A line chart showing device_coherence over time, with the line color changing based on the significance level at each data point.

#### 7.2.2 Color Specifications (Device Significance)

These colors match the physical LED ring on the NextGen RNG hardware:

| Significance Level | Chart Color | Hex Code | LED Color |
|-------------------|-------------|----------|-----------|
| **Normal** | Magenta | `#FF00FF` | Magenta |
| **Elevated** | Cyan | `#00FFFF` | Cyan |
| **High** | Yellow | `#FFFF00` | Yellow |
| **Very High** | Orange | `#FFA500` | Orange |
| **Extreme** | Gold | `#FFD700` | Gold |

**Alternative muted palette** (for better readability on white background):

| Significance Level | Muted Color | Hex Code |
|-------------------|-------------|----------|
| **Normal** | Steel Blue | `#4F6D7A` |
| **Elevated** | Sandy Brown | `#F4A261` |
| **High** | Terra Cotta | `#E76F51` |
| **Very High** | Crimson | `#C1121F` |
| **Extreme** | Dark Red | `#780000` |

**Implementation Note:** Offer a toggle between "Hardware LED Colors" and "Print-Friendly Colors." Default to the LED-matching colors for authenticity with the GCP2 hardware experience.

#### 7.2.3 Significance Threshold Lines

Draw horizontal dashed lines at each significance boundary:

```python
SIGNIFICANCE_THRESHOLDS = {
    "Elevated (p<0.1)":   243,
    "High (p<0.05)":      288,
    "Very High (p<0.01)": 378,
    "Extreme (p<0.001)":  483,
}
```

Each line should be drawn in the color of the level it begins, with a subtle dash pattern and a small label at the right margin.

#### 7.2.4 Axis Specifications

**X-Axis:**
- **Label:** `"Time"` or `"Date/Time"` (depending on range)
- **Format:** For ranges < 24 hours: `HH:MM`; for ranges > 24 hours: `YYYY-MM-DD HH:MM`
- **Timezone:** Display in user-selected timezone (default: Asia/Kolkata for IST)

**Y-Axis:**
- **Label:** `"Device Coherence"`
- **Range:** Auto-scaled with slight padding above max value
- **Zero visible:** Yes, include zero in range

#### 7.2.5 Annotations

- Mark the **peak coherence value** with a small annotation: `"Peak: {value} ({significance})"`
- If periods of Extreme significance exist, highlight those intervals with a semi-transparent background band

### 7.3 Multi-Device Comparison Chart

#### 7.3.1 Design

Overlay up to 4 device coherence lines on a single chart. Each device gets a distinct color from a colorblind-friendly palette.

#### 7.3.2 Color Palette (Up to 5 Devices)

| Device Slot | Color Name | Hex Code |
|-------------|-----------|----------|
| Device 1 | Navy | `#1D3557` |
| Device 2 | Steel Blue | `#457B9D` |
| Device 3 | Burnt Orange | `#E76F51` |
| Device 4 | Teal | `#2A9D8F` |
| Device 5 | Amethyst | `#7B2D8E` |

#### 7.3.3 Legend

- Use device names (if configured) instead of device numbers: e.g., `"Lab1 (Device 15)"` instead of `"Device 15"`
- Position legend at the top of the chart

#### 7.3.4 Time Alignment

All devices must be plotted against the **same time axis**. If devices have different date ranges, the chart should:
- Use the intersection of available time ranges
- Warn the user if time ranges do not overlap

### 7.4 Device-Network Correlation Chart (Dual-Axis)

#### 7.4.1 Design

When both Device Coherence and Network Coherence data are uploaded for overlapping time periods, produce a dual-axis chart:

- **Left Y-Axis:** Device Coherence (with significance coloring)
- **Right Y-Axis:** Cumulative Network Coherence (Red Curve + Blue Envelope)
- **Shared X-Axis:** Time in user-selected timezone

#### 7.4.2 Visual Separation

- Device coherence: area fill with low opacity (0.3) in device color
- Network cumsum: Red line overlaid
- Blue envelope: Dashed blue lines (to distinguish from device area)

#### 7.4.3 Correlation Highlights

When both Device and Network coherence show elevated significance simultaneously:
- Add a subtle **green-tinted background band** over those time intervals
- Include a text annotation: `"Correlated significance: [start_time] - [end_time]"`

### 7.5 Raw Network Coherence Chart

A simple line chart showing the raw (non-cumulative) network_coherence values over time:

- **Line color:** Medium blue `#457B9D`
- **Line width:** 1.5 px
- **Y-axis label:** `"Network Coherence"`
- **X-axis label:** `"Time"`
- **Zero line:** Visible horizontal dashed line

### 7.6 Chart Export Specifications

All charts must be exportable in:

| Format | Resolution | Use Case |
|--------|-----------|----------|
| **PNG** | 300 DPI, width 1600px | Presentation slides, web sharing |
| **PDF** | Vector, A4 landscape | Publication, archival |

Export includes:
- The chart itself
- Title and subtitle
- Legend
- Axis labels and tick marks
- A small footer: `"Generated by GCP2 Consciousness Data Analyzer | Data source: gcp2.net"`

---

## 8. Device Naming & Configuration System

### 8.1 Purpose

Users hosting multiple devices need meaningful labels instead of numeric IDs. The configuration system allows:

- Assign a custom name to any Device ID
- Names persist across sessions (saved to `device_config.json`)
- Names appear in all charts, reports, and analysis outputs

### 8.2 Data Model

```json
{
  "devices": {
    "15": {
      "name": "Lab1",
      "location": "HeartMath Lab, California",
      "notes": "Primary research device"
    },
    "337": {
      "name": "Control",
      "location": "HeartMath Lab, California",
      "notes": "Control device for comparison"
    },
    "53": {
      "name": "Lab2",
      "location": "Remote site",
      "notes": ""
    },
    "42": {
      "name": "Pyramid Bangalore",
      "location": "Bangalore, India",
      "notes": "Co-located with meditation center"
    }
  },
  "last_updated": "2026-04-11T10:30:00Z"
}
```

### 8.3 UI Workflow

1. **Initial Setup** (first visit or setup page):
   - App shows a table of all device IDs it has encountered
   - Each row has: Device ID (read-only), Name (editable), Location (editable), Notes (editable)
   - "Save Configuration" button persists to `device_config.json`

2. **Auto-Detection on Upload:**
   - When a device CSV is uploaded, the device_number is extracted
   - If device_number exists in config, use the saved name
   - If device_number is new, prompt: "New device detected: Device {id}. Would you like to name it?"

3. **Edit Existing Names:**
   - Accessible from sidebar: "Device Configuration" section
   - Table displays all known devices with inline editing
   - Changes take effect immediately in current session and are persisted

### 8.4 Display Format

In all charts and reports, devices are referenced as:

```
{custom_name} (Device {id})
```

Examples:
- `Lab1 (Device 15)`
- `Control (Device 337)`
- `Pyramid Bangalore (Device 42)`

If no custom name is set, fall back to:
- `Device {id}`

---

## 9. Analysis Engine & Report Generation

### 9.1 Device Activity Report

When a user uploads Device Coherence data and requests a report, the app generates a structured analysis of device activity within the selected date range.

#### 9.1.1 Report Structure

```
=================================================================
DEVICE ACTIVITY REPORT
=================================================================
Device:     Lab1 (Device 15)
Period:     2025-10-01 00:00 IST  to  2025-10-07 23:59 IST
Generated:  2026-04-11 14:30 IST
Data Rows:  10,080
Coverage:   98.2% (active_seconds / possible_seconds)
-----------------------------------------------------------------

SUMMARY STATISTICS
------------------
Mean Device Coherence:    87.3
Max Device Coherence:     512.7 (Extreme)
Min Device Coherence:     2.1
Std Deviation:            45.2

SIGNIFICANCE BREAKDOWN
-----------------------
Normal:     9,450 rows  (93.8%)
Elevated:     380 rows  ( 3.8%)
High:         150 rows  ( 1.5%)
Very High:     72 rows  ( 0.7%)
Extreme:       28 rows  ( 0.3%)

SIGNIFICANT PERIODS DETAIL
----------------------------
The following time periods showed elevated or higher significance:

  1. 2025-10-02 14:30 - 15:45 IST
     Peak: 512.7 (Extreme) at 15:02 IST
     Duration: 75 minutes above Elevated
     Active Seconds: 3600 (full coverage)

  2. 2025-10-04 08:00 - 09:30 IST
     Peak: 398.2 (Very High) at 08:45 IST
     Duration: 90 minutes above Elevated
     Active Seconds: 3540 (98.3%)

  3. 2025-10-05 20:15 - 21:00 IST
     Peak: 305.1 (High) at 20:32 IST
     Duration: 45 minutes above Elevated
     Active Seconds: 3600 (full coverage)

  [... additional periods ...]

DATA QUALITY NOTES
-------------------
- 3 rows had active_seconds < 3600 (possible partial hours)
- No data gaps detected > 120 seconds
- No duplicate timestamps found

=================================================================
```

#### 9.1.2 Significant Period Detection Algorithm

```python
def detect_significant_periods(df, min_significance="Elevated"):
    """
    Identify contiguous time periods where device_coherence
    meets or exceeds the given significance threshold.
    
    Returns list of dicts with:
      - start_time, end_time
      - peak_value, peak_time, peak_significance
      - duration_minutes
      - mean_active_seconds
    """
    significance_rank = {
        "Normal": 0, "Elevated": 1, "High": 2,
        "Very High": 3, "Extreme": 4
    }
    min_rank = significance_rank[min_significance]
    
    df["above_threshold"] = df["significance"].map(significance_rank) >= min_rank
    
    # Identify contiguous groups
    df["group"] = (df["above_threshold"] != df["above_threshold"].shift()).cumsum()
    
    periods = []
    for _, group_df in df[df["above_threshold"]].groupby("group"):
        peak_idx = group_df["device_coherence"].idxmax()
        periods.append({
            "start_time": group_df["datetime_display"].iloc[0],
            "end_time": group_df["datetime_display"].iloc[-1],
            "duration_minutes": len(group_df),  # ~1 row per minute
            "peak_value": group_df.loc[peak_idx, "device_coherence"],
            "peak_time": group_df.loc[peak_idx, "datetime_display"],
            "peak_significance": group_df.loc[peak_idx, "significance"],
            "mean_active_seconds": group_df["active_seconds"].mean(),
        })
    
    return periods
```

### 9.2 Network Coherence Report

When the user uploads Network Coherence data and selects a date/time range:

#### 9.2.1 Report Structure

```
=================================================================
NETWORK COHERENCE ANALYSIS REPORT
=================================================================
Network:    Global Network
Period:     2025-04-09 08:25:00 IST  to  2025-04-09 08:35:00 IST
Duration:   10 minutes (600 seconds)
Generated:  2026-04-11 14:30 IST
Data Points: 600 (1-second granularity)
Active Devices: 350-355 (range during window)
-----------------------------------------------------------------

CUMULATIVE SUM ANALYSIS
------------------------
Final Cumulative Value:  +72.4
Peak Cumulative Value:   +85.3 at 08:31:42 IST (minute 6.7)
Min Cumulative Value:    -3.2 at 08:25:15 IST (minute 0.25)
Direction:               Persistent upward trend

ENVELOPE ANALYSIS (95% Confidence)
-----------------------------------
Upper envelope at end of window:  +60.1
Lower envelope at end of window:  -60.1

SIGNIFICANCE ASSESSMENT:
  The cumulative sum EXITED the upper 95% confidence envelope
  at approximately minute 3.2 (08:28:12 IST) and remained
  above it for the remainder of the analysis window.
  
  This indicates STATISTICALLY SIGNIFICANT network coherence
  (p < 0.05) during this period.
  
  At peak: estimated p < 0.01

KEY INSIGHTS
-------------
1. Network coherence showed a clear upward trend beginning
   within the first minute of the analysis window
2. The red curve exited the blue envelope at minute 3.2,
   indicating the onset of statistically significant coherence
3. Coherence remained elevated throughout the duration
4. The persistent upward trend suggests sustained collective
   attention or emotional coherence across the network
5. Active device count remained stable (350-355), ruling out
   network topology changes as a confound

=================================================================
```

### 9.3 Combined Device + Network Correlation Report

When both data types are uploaded for overlapping time ranges, generate a correlation analysis:

#### 9.3.1 Report Structure

```
=================================================================
DEVICE-NETWORK CORRELATION REPORT
=================================================================
Device:     Lab1 (Device 15)
Network:    Global Network
Period:     2025-04-09 08:00 IST  to  2025-04-09 09:00 IST
Generated:  2026-04-11 14:30 IST
-----------------------------------------------------------------

TEMPORAL CORRELATION SUMMARY
------------------------------
Overlapping data points: 60 (device) / 3600 (network)
Time alignment: Device at ~1min intervals, Network at 1sec intervals

CONCURRENT SIGNIFICANCE WINDOWS:
  Period 1: 08:25 - 08:45 IST
    Device:  Elevated -> High (peak 305.2 at 08:32)
    Network: Cumsum exited envelope at 08:28
    Overlap: 17 minutes of simultaneous elevated activity
    
  Period 2: 08:50 - 08:58 IST
    Device:  Elevated (peak 267.1 at 08:54)
    Network: Cumsum still above envelope
    Overlap: 8 minutes of simultaneous elevated activity

CORRELATION ASSESSMENT:
  Device 15 showed elevated coherence during 25 of the 60 minutes
  in this window. Of those 25 minutes, 25 (100%) coincided with
  periods when the Network cumulative sum was above the 95%
  confidence envelope.
  
  This strong temporal overlap suggests that Device 15's local
  coherence was aligned with the global network signal during
  this period.

=================================================================
```

### 9.4 Report Generation Options

Users can choose from:

| Report Type | Required Data | Output |
|-------------|--------------|--------|
| **Device Activity Report** | 1 Device Coherence CSV | Text + optional PDF |
| **Multi-Device Comparison** | 2-5 Device Coherence CSVs | Text + optional PDF |
| **Network Event Analysis** | 1 Network Coherence CSV | Text + chart + optional PDF |
| **Device-Network Correlation** | 1+ Device CSV + 1 Network CSV | Text + dual chart + optional PDF |

---

## 10. User Interface & Experience Design

### 10.1 Page Layout

```
+------------------------------------------------------------------+
|  SIDEBAR (collapsible)                   MAIN CONTENT AREA       |
|  +------------------+  +--------------------------------------+  |
|  |                  |  |                                      |  |
|  | [App Logo/Title] |  |  WELCOME / DASHBOARD                |  |
|  |                  |  |                                      |  |
|  | --- UPLOAD ---   |  |  [Upload your CSV files to begin]   |  |
|  | [Upload CSV(s)]  |  |                                      |  |
|  |                  |  |  --- OR ---                          |  |
|  | --- FILES ---    |  |                                      |  |
|  | File 1: Dev 15   |  |  [Load Demo Data]                   |  |
|  | File 2: Dev 337  |  |                                      |  |
|  | File 3: Network  |  +--------------------------------------+  |
|  |                  |  |                                      |  |
|  | --- FILTERS ---  |  |  ANALYSIS TABS                      |  |
|  | Timezone: IST    |  |  [Device] [Network] [Correlation]   |  |
|  | Date range: ...  |  |                                      |  |
|  | Time range: ...  |  |  +----------------------------------+|  |
|  |                  |  |  |                                  ||  |
|  | --- DEVICES ---  |  |  |   CHART AREA                    ||  |
|  | [Configure Names]|  |  |                                  ||  |
|  |                  |  |  |   (Interactive Plotly chart)     ||  |
|  | --- ACTIONS ---  |  |  |                                  ||  |
|  | [Generate Report]|  |  +----------------------------------+|  |
|  | [Export Chart]   |  |                                      |  |
|  | [Save Analysis]  |  |  METRICS & BREAKDOWN                |  |
|  |                  |  |  [Summary stats] [Significance tbl] |  |
|  +------------------+  |                                      |  |
|                         |  REPORT OUTPUT                      |  |
|                         |  [Generated report text]            |  |
|                         |  [Download PNG] [Download PDF]      |  |
|                         +--------------------------------------+  |
+------------------------------------------------------------------+
```

### 10.2 Theme & Branding

```toml
# .streamlit/config.toml
[theme]
base = "light"
primaryColor = "#C1121F"           # HeartMath burgundy
backgroundColor = "#F7F4EA"        # Warm cream
secondaryBackgroundColor = "#E9F0F5" # Light blue-gray
textColor = "#172A3A"              # Dark slate
font = "sans serif"
```

### 10.3 User Workflow: Step-by-Step

#### Workflow A: Device Analysis Only

```
1. User opens app
2. User uploads 1-5 Device Coherence CSV files
3. App detects device IDs, prompts for names if new
4. Sidebar shows: uploaded files, timezone picker, date/time range
5. User selects filters
6. Main area shows:
   - Tab "Device": Individual device charts with significance coloring
   - Tab "Compare": Multi-device overlay chart
   - Metrics: Summary stats, significance breakdown table
7. User clicks "Generate Report"
8. App produces Device Activity Report with significant periods
9. User downloads chart (PNG/PDF) and/or report (PNG/PDF)
```

#### Workflow B: Network Analysis Only

```
1. User uploads Network Coherence CSV
2. App detects network type, extracts group name
3. Sidebar shows: timezone, date/time range pickers
4. App waits for user to select date/time range
5. User selects range (e.g., event start to event end)
6. Main area shows:
   - Tab "Raw": Raw network coherence line chart
   - Tab "Event Analysis": Red Curve + Blue Envelope chart
   - Metrics: Cumsum stats, envelope analysis
7. User optionally enters event title and start time
8. User clicks "Generate Report"
9. App produces Network Coherence Analysis Report
10. User downloads chart and/or report
```

#### Workflow C: Combined Analysis

```
1. User uploads Device CSV(s) AND Network Coherence CSV
2. App detects both types
3. App presents a prompt:
   "You have uploaded both Device and Network data. 
    Would you like to:
    a) Analyze them separately
    b) Compare and correlate them (requires overlapping date range)"
4. If user chooses (b):
   - App identifies overlapping time range
   - App shows date/time range selector pre-filled with overlap
5. Main area shows:
   - Tab "Device": Individual device analysis
   - Tab "Network": Network event analysis
   - Tab "Correlation": Dual-axis chart + correlation report
6. User clicks "Generate Correlation Report"
7. App identifies periods of simultaneous significance
8. User downloads combined report and charts
```

### 10.4 Empty States & Help

When no files are uploaded, show:

```
Welcome to the GCP2 Consciousness Data Analyzer

This tool helps you analyze RNG data from the Global Consciousness Project 2.0.

Getting Started:
1. Go to gcp2.net > Data & Results > Data Download
2. Download Device Coherence CSV for your device(s)
3. Download Network Coherence CSV for the time period you want to analyze
4. Upload the files using the sidebar

What This Tool Can Do:
- Analyze device coherence patterns and identify significant periods
- Generate Event Analysis charts (Red Curve + Blue Envelope)
- Compare multiple devices side by side
- Correlate device activity with network coherence
- Generate detailed reports and export charts

Need sample data? Click "Load Demo Data" below to try the app
with pre-loaded data from Device 337 and the Global Network.

[Load Demo Data]
```

---

## 11. Multi-File Upload & Data Management

### 11.1 Upload Capabilities

| Feature | Specification |
|---------|--------------|
| Max files per upload | 10 |
| Accepted formats | `.csv`, `.zip` (containing CSV) |
| Max file size | 200 MB per file (Streamlit default) |
| Simultaneous types | Device + Network in same upload batch |

### 11.2 File Management Session State

```python
# Session state structure
st.session_state["uploaded_datasets"] = {
    "device_files": {
        "Device_15": ParsedDataset(...),
        "Device_337": ParsedDataset(...),
        "Device_53": ParsedDataset(...),
    },
    "network_files": {
        "Global_Network_2026_03": ParsedDataset(...),
    },
}
```

### 11.3 Upload Handling Logic

```
For each uploaded file:
  1. Attempt to read as CSV (or extract from ZIP)
  2. Detect type: device or network
  3. If device:
     - Extract device_number from data
     - Check if device already uploaded (warn if duplicate)
     - Add to device_files dict keyed by device label
  4. If network:
     - Extract group name from filename
     - Check if group already uploaded
     - Add to network_files dict
  5. If unknown:
     - Show error: "Could not identify file type. Expected columns: ..."
     - List expected columns for each type
```

### 11.4 Multiple Device Analysis

When 2+ device files are uploaded:

1. **Individual Analysis:** Each device gets its own tab/section with full analysis
2. **Comparison View:** An overlay chart with all devices on the same axes
3. **Table View:** Side-by-side significance breakdown for all devices
4. **Time Alignment:** Only show the overlapping time range in comparison view

### 11.5 Data Persistence Within Session

- Uploaded data persists in `st.session_state` for the duration of the browser session
- Changing filters does NOT require re-uploading files
- A "Clear All Data" button resets the session
- Individual files can be removed via an "X" button next to each file listing

---

## 12. Export & Download System

### 12.1 Chart Downloads

| Format | Method | Quality |
|--------|--------|---------|
| **PNG** | `fig.to_image(format="png", width=1600, height=900, scale=2)` via kaleido | 300 DPI equivalent |
| **PDF** | `fig.to_image(format="pdf", width=1600, height=900)` via kaleido | Vector |

**File naming convention:**
```
GCP2_{chart_type}_{device_or_network}_{date_range}_{timestamp}.{ext}
```
Example: `GCP2_EventAnalysis_GlobalNetwork_20250409_08h25_to_08h35_20260411_143000.png`

### 12.2 Report Downloads

Reports should be downloadable in two formats:

| Format | Method | Use Case |
|--------|--------|----------|
| **PNG** | Render report text as an image with proper formatting | Quick sharing |
| **PDF** | Generate formatted PDF document using fpdf2 or reportlab | Archival, professional |

**PDF Report Structure:**
```
Page 1: Cover
  - Title: "GCP2 Data Analysis Report"
  - Event name, date range, device info
  - Generated date
  - "Data source: gcp2.net"

Page 2+: Analysis Content
  - Summary statistics
  - Significance breakdown table
  - Significant period details
  - Charts embedded as images

Final Page: Methodology Note
  - Brief explanation of GCP2 methodology
  - Reference to data_download_calculations.pdf
  - Link to gcp2.net
```

### 12.3 Filtered Data Downloads

Users can download the filtered dataset as CSV:

```python
csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data (CSV)",
    data=csv_bytes,
    file_name=f"GCP2_filtered_{dataset_label}_{date_range}.csv",
    mime="text/csv",
)
```

### 12.4 Save Analysis Session

Save analysis metadata for future reference:

```json
{
  "title": "World Navkar Mantra Day Analysis",
  "event_name": "Navkar Mantra Chanting",
  "created_utc": "2026-04-11T09:00:00Z",
  "timezone_display": "Asia/Kolkata",
  "date_range": {
    "start": "2025-04-09T08:25:00+05:30",
    "end": "2025-04-09T08:35:00+05:30"
  },
  "datasets": [
    {
      "type": "network",
      "group": "Global Network",
      "rows": 600,
      "filename": "network_navkar.csv"
    }
  ],
  "metrics": {
    "final_cumsum": 72.4,
    "peak_cumsum": 85.3,
    "envelope_exit_minute": 3.2,
    "significance": "Significant (p < 0.05)"
  },
  "notes": "Strong upward trend during chanting portion. Red curve clearly exited envelope."
}
```

---

## 13. Deployment & GitHub Repository

### 13.1 Repository Setup

**Repository Name:** `gcp2-analyzer` (or `GCP2_Data` if using existing)

**Public Repository Checklist:**

- [ ] Public visibility enabled
- [ ] README.md with:
  - Project description
  - Live app link
  - Screenshot of the app
  - Getting started guide
  - How to contribute
- [ ] LICENSE file (MIT recommended for open-source citizen science)
- [ ] `.gitignore` (Python, Streamlit, IDE files)
- [ ] `requirements.txt` pinned to compatible versions
- [ ] `.streamlit/config.toml` with theme
- [ ] No secrets, API keys, or personal data in repo
- [ ] Sample data included in `resources/` for demo mode

### 13.2 Streamlit Community Cloud Deployment

1. Push code to GitHub public repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub account
4. Select repository and `app.py` as main file
5. Deploy -- generates public URL like `https://gcp2-analyzer.streamlit.app`

**Configuration for deployment:**
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### 13.3 Access Model

- **No authentication required** -- anyone with the link can use the app
- **No data stored server-side** -- all uploads are session-local
- **No user accounts** -- the app is stateless between visits
- Device configuration is session-local (persists via browser session state, not server storage)

**Note on Streamlit Cloud Limitations:**
- Session state resets when the app sleeps (after ~15 min of inactivity)
- File uploads are limited by Streamlit's maxUploadSize setting
- Device configurations will not persist across sessions on cloud deployment -- consider offering config export/import as JSON

---

## 14. Project Plan & Milestones

### Phase 1: Foundation (Weeks 1-2)

| Task | Description | Deliverable |
|------|-------------|-------------|
| 1.1 | Set up GitHub public repo with proper structure | Repo with README, .gitignore, requirements |
| 1.2 | Implement CSV parser with device/network auto-detection | parsers.py with tests |
| 1.3 | Implement time utilities (UTC conversion, timezone display, filtering) | time_utils.py with tests |
| 1.4 | Build basic Streamlit app shell with file upload | Running app.py skeleton |
| 1.5 | Implement device configuration system | device_config.py, device_config.json |
| 1.6 | Add demo data loading | demo_data.py with bundled samples |

### Phase 2: Device Analysis (Weeks 3-4)

| Task | Description | Deliverable |
|------|-------------|-------------|
| 2.1 | Implement device analysis engine | device_analysis.py with summary, breakdown |
| 2.2 | Build Device Coherence timeline chart (significance-colored) | plots.py device charts |
| 2.3 | Build multi-device comparison chart | plots.py multi-device overlay |
| 2.4 | Implement significant period detection algorithm | Analysis engine |
| 2.5 | Build Device Activity Report generator | reports.py device report |
| 2.6 | Add significance threshold lines to device charts | Chart enhancement |

### Phase 3: Network Analysis (Weeks 5-6)

| Task | Description | Deliverable |
|------|-------------|-------------|
| 3.1 | Implement network analysis engine (cumsum, envelope) | network_analysis.py |
| 3.2 | Build Event Analysis chart (Red Curve + Blue Envelope) -- **exact GCP2.net match** | plots.py network chart |
| 3.3 | Implement relative time axis (minutes from event start) | Time conversion logic |
| 3.4 | Add event title and start time configuration | UI for event metadata |
| 3.5 | Build Network Coherence Analysis Report generator | reports.py network report |
| 3.6 | Validate envelope calculations against known events | Test suite with reference data |

### Phase 4: Correlation & Comparison (Weeks 7-8)

| Task | Description | Deliverable |
|------|-------------|-------------|
| 4.1 | Implement Device-Network correlation engine | correlation_analysis.py |
| 4.2 | Build dual-axis correlation chart | plots.py correlation chart |
| 4.3 | Implement simultaneous significance detection | Correlation algorithm |
| 4.4 | Build Correlation Report generator | reports.py correlation report |
| 4.5 | Handle time alignment between device (~1min) and network (1sec) data | Time resampling logic |

### Phase 5: Export, Polish & Deploy (Weeks 9-10)

| Task | Description | Deliverable |
|------|-------------|-------------|
| 5.1 | Implement PNG/PDF chart export | kaleido integration |
| 5.2 | Implement PDF report generation | fpdf2/reportlab integration |
| 5.3 | Implement analysis session saving | storage.py with JSON |
| 5.4 | Add device config export/import (JSON) | UI for config portability |
| 5.5 | UI polish: empty states, help text, error messages | UX improvements |
| 5.6 | Deploy to Streamlit Community Cloud | Live public URL |
| 5.7 | Write comprehensive README | Documentation |

### Phase 6: Validation & Refinement (Weeks 11-12)

| Task | Description | Deliverable |
|------|-------------|-------------|
| 6.1 | Validate all charts against GCP2.net Event Analysis screenshots | Visual comparison |
| 6.2 | Test with real data from known significant events | Accuracy verification |
| 6.3 | Run full test suite | All tests passing |
| 6.4 | Community beta testing (share with GCP2 forum) | Feedback collection |
| 6.5 | Bug fixes and chart refinements based on feedback | Polished release |

---

## 15. Testing & Validation Strategy

### 15.1 Unit Tests

```python
# test_network_math.py

def test_envelope_increases_with_time():
    """Envelope must widen as degrees of freedom increase."""
    df = create_test_network_data(seconds=1000)
    metrics = add_network_metrics(df)
    assert metrics["envelope_upper"].is_monotonic_increasing

def test_envelope_is_symmetric():
    """Upper and lower envelopes must be exact mirrors."""
    df = create_test_network_data(seconds=500)
    metrics = add_network_metrics(df)
    np.testing.assert_array_almost_equal(
        metrics["envelope_upper"], -metrics["envelope_lower"]
    )

def test_cumsum_of_zeros_stays_at_zero():
    """If all coherence values are 0, cumsum should be 0."""
    df = create_zero_network_data(seconds=100)
    metrics = add_network_metrics(df)
    assert (metrics["cumulative_coherence"] == 0).all()

def test_significance_thresholds():
    """Verify the exact threshold values from documentation."""
    assert classify_significance(242) == "Normal"
    assert classify_significance(243) == "Elevated"
    assert classify_significance(287) == "Elevated"
    assert classify_significance(288) == "High"
    assert classify_significance(377) == "High"
    assert classify_significance(378) == "Very High"
    assert classify_significance(482) == "Very High"
    assert classify_significance(483) == "Extreme"

def test_degrees_of_freedom_equals_elapsed_seconds():
    """At second N, df must equal N."""
    df = create_test_network_data(seconds=100)
    metrics = add_network_metrics(df)
    # Verify envelope is calculated with correct df
    expected_upper = np.sqrt(chi2.ppf(0.95, np.arange(1, 101)))
    np.testing.assert_array_almost_equal(
        metrics["envelope_upper"].values, expected_upper
    )
```

### 15.2 Visual Validation Against Known Events

Use these documented events as test cases to verify chart output matches known results:

| Event | Date | Expected Behavior | Reference |
|-------|------|-------------------|-----------|
| World Navkar Mantra Day - chanting | 2025-04-09 08:25 IST | Red Curve exits upper envelope, stays above | Reference image in resources/ |
| Mahayog Dhyan Kumbh - Meditation 2 (Music) | 2025-10-05 | Clearly significant, sharp upward trajectory | PPTX in resources/ |
| Mahayog Dhyan Kumbh - Meditation 7 (Music) | 2025-10-xx | Significant, clears upper 95% CI | PPTX in resources/ |
| Tibetan Bowls meditation | 2025-10-04 | Downward trend, stays within envelope | GCP2 community reports |
| September 11, 2001 (GCP 1.0) | 2001-09-11 | Extreme significance, odds > 1 in 1,000 | GCP 1.0 benchmark |
| Global Spirituality Mahotsav | March 2024 | Foundational GCP 2.0 test event | GCP2 research papers |

### 15.3 Chart Pixel Comparison

For the Network Event Analysis chart specifically:

1. Generate chart from known event data
2. Compare against the reference screenshot (`full_whitening_World_Navkar_Mantra_Day_-_chanting_20250409.png`)
3. Verify:
   - Red curve trajectory matches
   - Blue envelope parabolic shape matches
   - Axis labels and ranges match
   - Title format matches
   - Zero line and event marker present

### 15.4 Integration Tests

```python
def test_full_device_workflow():
    """Upload device CSV -> filter -> analyze -> export."""
    raw = load_test_device_csv()
    parsed = parse_uploaded_file(raw, "device_337.csv")
    assert parsed.dataset_type == "device"
    
    filtered = filter_by_date_and_time(parsed.df, ...)
    summary = device_summary(filtered)
    assert summary["rows"] > 0
    
    fig = device_line_figure(filtered, "Test Device")
    img = fig.to_image(format="png")
    assert len(img) > 0

def test_full_network_workflow():
    """Upload network CSV -> filter -> cumsum -> envelope -> export."""
    raw = load_test_network_csv()
    parsed = parse_uploaded_file(raw, "network_global.csv")
    assert parsed.dataset_type == "network"
    
    filtered = filter_by_date_and_time(parsed.df, ...)
    metrics = add_network_metrics(filtered)
    assert "cumulative_coherence" in metrics.columns
    assert "envelope_upper" in metrics.columns
    
    fig = network_event_analysis_chart(metrics, "Test Event", ...)
    img = fig.to_image(format="png")
    assert len(img) > 0
```

---

## 16. Reference Materials & External Sources

### 16.1 Primary Sources (Must-Follow)

| Source | Purpose | URL / Path |
|--------|---------|------------|
| **data_download_calculations.pdf** | Official calculation methodology | `/resources/data_download_calculations.pdf` |
| **GCP2.net Event Analysis** | Reference for chart formatting | `https://gcp2.net/data-results/event-analysis` |
| **GCP2 Playbox - Basic Cumsum Plot** | Reference Python implementation | `https://github.com/vfp2/gcp2-playbox/tree/main/experiments/1-basic-cumsum-plot` |
| **World Navkar Mantra Day reference chart** | Visual benchmark for Event Analysis chart | `/resources/full_whitening_World_Navkar_Mantra_Day_-_chanting_20250409.png` |

### 16.2 Secondary Sources (Context & Research)

| Source | Purpose |
|--------|---------|
| **GCP RNG Statistical Analysis Explorer** (`gcpeggs.fp2.dev`) | Alternative visualization approach (Dash-based) |
| **GCP Experiments Portal** (`gcp.fp2.dev`) | Community experiment portal |
| **Mind-Matter Interaction Forum** | Community discussion and analysis methods |
| **Bancel & Nelson (2008), Journal of Scientific Exploration** | Mathematical foundation for coherence/variance metrics |
| **GCP2 Playbox - Financial Backtesting** | Advanced analysis patterns (Stouffer-Z, group_id partitioning) |
| **ScienceDirect paper** (2025) | Recent peer-reviewed research on consciousness-coherence |
| **Mahayog Dhyan Kumbh PPTX** | Event analysis examples with chart visuals |
| **GCP2 FAQ documents** (RNG_FAQ_1/2/3.md) | Technical Q&A from Rollin McCraty |

### 16.3 Hardware Reference

| Document | Purpose |
|----------|---------|
| **TrueRNG spec v3.docx** | RNG hardware specifications |
| **RNG GCP2.0.pdf** | RNG system design document |
| **GCP2 device security statement** | Security architecture |
| **Quick Start Guide / User Manual** | User-facing device documentation |

---

## 17. Appendices

### Appendix A: Complete Constants Reference

```python
# constants.py -- Single source of truth for all app constants

# ============================================================
# SIGNIFICANCE THRESHOLDS (from data_download_calculations.pdf)
# ============================================================
SIGNIFICANCE_THRESHOLDS = {
    "Normal":    {"min": 0,   "max": 242,  "p_value": "> 0.1"},
    "Elevated":  {"min": 243, "max": 287,  "p_value": "< 0.1"},
    "High":      {"min": 288, "max": 377,  "p_value": "< 0.05"},
    "Very High": {"min": 378, "max": 482,  "p_value": "< 0.01"},
    "Extreme":   {"min": 483, "max": None, "p_value": "< 0.001"},
}

SIGNIFICANCE_ORDER = ["Normal", "Elevated", "High", "Very High", "Extreme"]

# ============================================================
# CHART COLORS -- EVENT ANALYSIS (GCP2.net match)
# ============================================================
EVENT_CHART_COLORS = {
    "red_curve":        "#FF0000",   # Cumulative sum line
    "blue_envelope":    "#0000FF",   # 95% confidence interval
    "zero_baseline":    "#000000",   # Horizontal zero line
    "event_marker":     "#000000",   # Vertical event start line
    "background":       "#FFFFFF",   # Chart background
    "grid":             "#E0E0E0",   # Grid lines
}

# ============================================================
# CHART COLORS -- DEVICE SIGNIFICANCE (Hardware LED Match)
# ============================================================
DEVICE_LED_COLORS = {
    "Normal":    "#FF00FF",  # Magenta
    "Elevated":  "#00FFFF",  # Cyan
    "High":      "#FFFF00",  # Yellow
    "Very High": "#FFA500",  # Orange
    "Extreme":   "#FFD700",  # Gold
}

# Muted palette for print/white-background readability
DEVICE_MUTED_COLORS = {
    "Normal":    "#4F6D7A",  # Steel Blue
    "Elevated":  "#F4A261",  # Sandy Brown
    "High":      "#E76F51",  # Terra Cotta
    "Very High": "#C1121F",  # Crimson
    "Extreme":   "#780000",  # Dark Red
}

# ============================================================
# CHART COLORS -- MULTI-DEVICE COMPARISON
# ============================================================
MULTI_DEVICE_PALETTE = [
    "#1D3557",  # Navy
    "#457B9D",  # Steel Blue
    "#E76F51",  # Burnt Orange
    "#2A9D8F",  # Teal
    "#7B2D8E",  # Amethyst
]

# ============================================================
# CHART DIMENSIONS
# ============================================================
CHART_HEIGHT_STANDARD = 520       # pixels
CHART_HEIGHT_COMPACT = 420        # pixels
CHART_WIDTH_EXPORT = 1600         # pixels for PNG/PDF export
CHART_HEIGHT_EXPORT = 900         # pixels for PNG/PDF export
CHART_EXPORT_SCALE = 2            # 2x for high-DPI

# ============================================================
# CHART LINE WIDTHS
# ============================================================
LINE_WIDTH_RED_CURVE = 1.5
LINE_WIDTH_BLUE_ENVELOPE = 1.5
LINE_WIDTH_ZERO_BASELINE = 1.0
LINE_WIDTH_EVENT_MARKER = 1.5
LINE_WIDTH_DEVICE_LINE = 2.0
LINE_WIDTH_THRESHOLD = 1.0

# ============================================================
# CONFIDENCE INTERVAL
# ============================================================
CONFIDENCE_LEVEL = 0.95           # 95% for the Blue Envelope
CONFIDENCE_LEVEL_NEAR_SIG = 0.90  # 90% for "Near Significant"
CONFIDENCE_LEVEL_VERY_SIG = 0.99  # 99% for "Very Significant"
CONFIDENCE_LEVEL_EXTREME = 0.999  # 99.9% for "Extreme"

# ============================================================
# DATA CONSTANTS
# ============================================================
DEVICE_INTERVAL_SECONDS = 60      # ~1 row per minute for device data
NETWORK_INTERVAL_SECONDS = 1      # 1 row per second for network data
MAX_ACTIVE_SECONDS = 3600         # Full hour of device uptime
RNGS_PER_DEVICE = 4               # 4 RNGs in each NextGen device
RNGS_USED_FOR_COHERENCE = 3       # 3 of 4 used (4th sequestered)

# ============================================================
# TIMEZONE DEFAULTS
# ============================================================
DEFAULT_DISPLAY_TIMEZONE = "Asia/Kolkata"
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
# UI CONSTANTS
# ============================================================
MAX_DEVICE_UPLOADS = 5
MAX_COMPARISON_DEVICES = 4
MAX_FILE_SIZE_MB = 200
DEMO_DEVICE_FILE = "resources/GCP2_Device_Coherence_Device_337_Latest.csv"
DEMO_NETWORK_FILE = "resources/GCP2_Network_Coherence_Global_Network_2026_03.csv.zip"
```

### Appendix B: Envelope Calculation -- Step-by-Step Walkthrough

For a network coherence analysis window of 600 seconds (10 minutes):

```python
import numpy as np
from scipy.stats import chi2

# Step 1: Create degrees of freedom array (1 to 600)
n = np.arange(1, 601)

# Step 2: For each second, find the chi-squared value at 95%
# This asks: "What chi-squared value would 95% of random data fall below
# if we had n degrees of freedom?"
chi2_values = chi2.ppf(0.95, n)

# Step 3: Take square root to convert from variance to standard deviation scale
# The cumulative sum operates on the standard deviation scale
envelope_upper = np.sqrt(chi2_values)
envelope_lower = -envelope_upper

# Step 4: Verify the parabolic shape
# At n=1:   envelope = sqrt(chi2.ppf(0.95, 1))   = sqrt(3.841)  = 1.960
# At n=60:  envelope = sqrt(chi2.ppf(0.95, 60))   = sqrt(79.08)  = 8.893
# At n=600: envelope = sqrt(chi2.ppf(0.95, 600))  = sqrt(660.7)  = 25.70

# The envelope grows as approximately sqrt(n), creating the parabolic shape
```

### Appendix C: Reference Chart Comparison Checklist

When validating that your generated chart matches the GCP2.net reference:

- [ ] **Red Curve** is pure red (#FF0000), not burgundy or orange
- [ ] **Blue Envelope** is pure blue (#0000FF), not navy or teal
- [ ] **Envelope is parabolic** (wider at right than left)
- [ ] **Upper and lower envelope are symmetric** around zero
- [ ] **X-axis shows minutes** (not seconds, not timestamps)
- [ ] **X-axis starts at 0.0** (or slightly negative if pre-event data included)
- [ ] **Y-axis label** reads "Network Coherence (P)"
- [ ] **Zero line** is visible as a solid horizontal line
- [ ] **Event marker** is a vertical line at x=0
- [ ] **Title** includes event name on line 1, start time with timezone on line 2
- [ ] **Background** is white, not gray or colored
- [ ] **Grid** is subtle light gray, not dominant
- [ ] **Red curve starts near zero** and develops its trend over time
- [ ] **Envelope starts narrow** (near the origin) and widens
- [ ] **When Red Curve exits envelope**, the crossing point is clearly visible
- [ ] **Chart is legible** at 1600px wide export resolution

### Appendix D: Known Data Quality Issues

From GCP2.net documentation, certain dates have missing or corrupted data due to technical issues. The app should:

1. Warn users if their selected date range includes known-bad dates
2. Not crash or produce misleading results from bad data
3. Clearly mark gaps in the time series on charts

### Appendix E: Glossary

| Term | Definition |
|------|-----------|
| **RNG** | Random Number Generator; the physical hardware producing quantum random bits |
| **NextGen RNG** | The GCP 2.0 hardware device containing 4 RNGs with LED ring |
| **Device Coherence** | Smoothed measure of intra-device RNG synchronization (3 of 4 RNGs) |
| **Network Coherence** | Measure of inter-device synchronization across the network |
| **CUMSUM** | Cumulative Sum; running total of coherence values over time |
| **Red Curve** | Visual representation of the cumulative sum in Event Analysis charts |
| **Blue Envelope** | 95% confidence interval boundary for the cumulative sum |
| **Degrees of Freedom (df)** | Number of seconds elapsed from analysis window start |
| **Chi-squared (chi2)** | Statistical distribution used to model random RNG output |
| **p-value** | Probability that observed data could occur by pure chance |
| **Citizen Scientist** | Volunteer who hosts an RNG device and contributes data |
| **EGG** | Electrogaiagram; alternate name for RNG device (GCP 1.0 terminology) |
| **NetVar** | Network Variance; original GCP 1.0 name for Network Coherence metric |
| **Whitening** | Process applied to raw RNG output to ensure statistical baseline quality |
| **Anti-coherence** | Significant departure from randomness in the negative direction |
| **Stouffer-Z** | Statistical method used in GCP 1.0 for per-second calculations |

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-11 | Ramesh Guda | Initial comprehensive specification |
| 2.0 | 2026-04-11 | Ramesh Guda + Claude | Expanded with full technical specs, chart plotting single source of truth, mathematical foundations, all constants and color codes |

---

*This document is the canonical reference for the GCP2 Consciousness Data Analyzer application. All development, chart rendering, mathematical calculations, and visual design decisions must conform to the specifications herein. When in doubt, refer to the data_download_calculations.pdf and the reference chart images in the resources/ directory.*
