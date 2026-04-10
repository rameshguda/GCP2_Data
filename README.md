# GCP2 Consciousness Data Analyzer

A free, publicly accessible web application for analyzing Random Number Generator (RNG) data from the [Global Consciousness Project 2.0](https://gcp2.net).

## What It Does

- Upload **Device Coherence** and **Network Coherence** CSV files from gcp2.net
- Analyze device activity and identify periods of statistical significance
- Generate **Event Analysis charts** (Red Curve + Blue Envelope) matching GCP2.net
- Compare multiple devices side by side
- Correlate device coherence with global network coherence
- Generate detailed reports and export charts as PNG/PDF

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
git clone https://github.com/rameshguda/gcp2-analyzer.git
cd gcp2-analyzer
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Get Data

1. Go to [gcp2.net](https://gcp2.net) > Data & Results > Data Download
2. Download **Device Coherence** CSV for your device(s)
3. Download **Network Coherence** CSV for the time period you want to analyze
4. Upload the files in the app sidebar

## Technical Reference

See [GCP2_APP_DEVELOPMENT_PROMPT.md](GCP2_APP_DEVELOPMENT_PROMPT.md) for the complete technical specification, including:

- Mathematical foundations (cumulative sum, chi-squared envelope, significance thresholds)
- Chart plotting specifications (exact colors, axes, visual components)
- Data schema and ingestion details
- Analysis engine and report generation specs

## Data Sources

All data comes from CSV files downloaded from [gcp2.net](https://gcp2.net). This app does not connect to any external APIs or store user data.

### Supported File Types

| File Type | Columns | Granularity |
|-----------|---------|-------------|
| Device Coherence | device_number, epoch_time_utc, active_seconds, device_coherence, significance | ~1 min |
| Network Coherence | epoch_time_utc, network_coherence, active_devices | 1 sec |

## License

MIT

## Acknowledgments

- [Global Consciousness Project 2.0](https://gcp2.net) for the data and scientific methodology
- [HeartMath Institute](https://www.heartmath.org) for research and device hosting
- [vfp2/gcp2-playbox](https://github.com/vfp2/gcp2-playbox) for reference implementations
- Bancel & Nelson (2008), Journal of Scientific Exploration, for the mathematical foundations
