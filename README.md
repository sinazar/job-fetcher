# job-fetcher

Daily fetcher for the Claude "Job Hunter" digest.

**How it works**
1. GitHub Actions runs `fetch_jobs.py` every night at 07:17 UTC (3:17 AM Toronto in summer, 2:17 AM in winter). GitHub often starts scheduled runs late, sometimes by hours, so the schedule leaves a wide buffer.
2. It pulls recently posted roles from JSearch (LinkedIn, Indeed, Glassdoor and company sites via Google for Jobs), RemoteOK, We Work Remotely and, optionally, Adzuna.
3. It applies cheap keyword filters (title, seniority, GTA or remote), skips anything it has already seen, and commits the results to `data/daily/YYYY-MM-DD.json` and `data/latest.json`.
4. At 9:13 AM Toronto a Claude scheduled task reads every `data/daily/YYYY-MM-DD.json` from the last 3 days (not just `latest.json`), skips job IDs already in the Google Sheet tracker, scores the rest against the master resume, adds them to the tracker and emails the digest. A fetch that lands after the digest is picked up the next morning.

No AI calls happen in this repo.

## Setup
1. Get a RapidAPI key and subscribe to **JSearch** (free BASIC plan): rapidapi.com → search "JSearch" → Subscribe → copy `X-RapidAPI-Key`.
2. In this repo go to **Settings → Secrets and variables → Actions → New repository secret** and add `RAPIDAPI_KEY`.
3. Optional: free Adzuna key from developer.adzuna.com → add the `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` secrets. If they're missing, Adzuna is skipped.
4. **Actions** tab → "Fetch jobs" → **Run workflow** to test. A `data/` commit should appear within a minute or two.

## Tuning
Everything is in `config.py`: the JSearch queries and pages per query, title include and exclude words, GTA cities and the remote regions to exclude. Keep the filters loose, since Claude does the real scoring.

Quota: 2 broad JSearch queries × 10 pages each. A 2–10 page request counts as 2, so that's ~4 requests/day ≈ 120 of the 200 free monthly requests. Remove the US-remote query to halve it.

## Run locally
```
pip install -r requirements.txt
RAPIDAPI_KEY=... python fetch_jobs.py
```

## Tune filters without spending API credits
Each run saves the raw JSearch responses to `data/raw_jsearch_latest.json`. After editing `config.py`, run

```
python fetch_jobs.py --replay
```

This re-applies the filters to the saved responses with no JSearch calls and writes `data/replay.json`. It doesn't touch the seen-jobs list.
