# GCP2 Data Analysis App

Streamlit application for exploring GCP 2.0 Device Coherence and Network Coherence CSV downloads.

## Current V1 foundation

- upload `csv` or zipped `csv` files
- detect `device` vs `network` data
- filter by date range and time-of-day
- display device and network charts
- compare up to 4 device files
- export filtered data to CSV
- export charts to PNG
- save analysis metadata locally
- use bundled demo data for quick evaluation

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Public deployment

This repository is designed to be deployed as a public Streamlit app.

Recommended path:

1. Push this repository to GitHub
2. Connect the GitHub repo to Streamlit Community Cloud
3. Deploy `app.py`
4. Share the public app URL with users

Anyone with the deployed app link will be able to open the app, upload their own data files, and run the analysis in the browser.

See also:

- [Deployment guide](/Users/heartmath/Documents/GCP2_Data/DEPLOYMENT.md)

## Sample files

Place GCP2 sample files in `resources/`.

Currently validated against:

- `GCP2_Device_Coherence_Device_337_Latest.csv`
- `GCP2_Network_Coherence_Global_Network_2026_03.csv.zip`
