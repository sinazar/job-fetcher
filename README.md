# job-fetcher

Daily fetcher for the Claude "Job Hunter" digest.

**How it works**
1. GitHub Actions runs `fetch_jobs.py` every morning (6:30 AM Toronto).
2. It pulls roles posted in the last ~24h from JSearch (LinkedIn, Indeed, Glassdoor and company sites via Google for Jobs), RemoteOK, We Work Remotely and, optionally, Adzuna.
3. It applies cheap keyword filters (title, seniority, GTA or remote), skips anything it has already seen, and commits the results to `data/daily/YYYY-MM-DD.json` and `data/latest.json`.
4. At 8:00 AM a Claude scheduled task reads `data/latest.json`, scores each role against the master resume, adds them to the Google Sheet tracker and emails the digest.

No AI calls happen in this repo.

## Setup
1. Get a RapidAPI key and subscribe to **JSearch** (free BASIC plan): rapidapi.com → search "JSearch" → Subscribe → copy `X-RapidAPI-Key`.
2. In this repo go to **Settings → Secrets and variables → Actions → New repository secret** and add `RAPIDAPI_KEY`.
3. Optional: free Adzuna key from developer.adzuna.com → add the `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` secrets. If they're missing, Adzuna is skipped.
4. **Actions** tab → "Fetch jobs" → **Run workflow** to test. A `data/` commit should appear within a minute or two.

## Tuning
Everything is in `config.py`: the JSearch queries (each one uses 1 request per day), title include and exclude words, GTA cities and the remote regions to exclude. Keep the filters loose, since Claude does the real scoring.

Quota: 4 JSearch queries × 30 days ≈ 120 of the 200 free monthly requests.

## Run locally
```
pip install -r requirements.txt
RAPIDAPI_KEY=... python fetch_jobs.py
```
