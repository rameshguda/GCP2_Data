# Deployment Guide

## Goal

Deploy this repository as a public Streamlit app so anyone with the app link can open it in a browser, upload their own GCP2 data files, and run the analysis.

## Hosting Model

- GitHub hosts the source code
- Streamlit Community Cloud hosts the running app
- Users access the Streamlit deployment URL

This means:

- GitHub URL = code repository
- App URL = usable analysis tool

## Recommended Public Deployment Steps

1. Push this repository to GitHub
2. Ensure `app.py` is the app entrypoint
3. Ensure `requirements.txt` is present in the repo root
4. Create a Streamlit Community Cloud deployment connected to this GitHub repo
5. Set the main file path to `app.py`
6. Deploy and test the public URL
7. Share the app URL with users

## What Users Will Be Able To Do

After deployment, any person with the app link will be able to:

- open the app in a browser
- upload their own CSV or ZIP data files
- filter by date and time
- analyze device and network coherence
- export filtered data and charts

## Important Public Access Notes

- A public deployment means anyone with the app link can use it
- Uploaded files may pass through the hosting platform during processing
- Before broad sharing, confirm that the uploaded datasets are appropriate for a public app workflow

## Pre-Deployment Checklist

- [ ] App starts successfully with `streamlit run app.py`
- [ ] Tests pass with `python -m pytest -q`
- [ ] `requirements.txt` is complete
- [ ] `.gitignore` excludes local and temporary files
- [ ] Demo mode works
- [ ] Sample upload flow works
- [ ] Export buttons work

## Local Verification Commands

```bash
source .venv/bin/activate
python -m pytest -q
python -m streamlit run app.py
```

## Suggested First Public Test

Before sharing with all users:

1. deploy the app
2. test it yourself with both sample datasets
3. ask 1 trusted user to try it
4. refine any confusing areas
5. then share with the remaining users
