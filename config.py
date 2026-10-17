"""
Search settings for the daily fetcher. Edit this file to change what gets pulled.

The fetcher is deliberately "dumb": it casts a reasonably wide net using cheap
keyword rules. Fit scoring, judgment and the digest happen in Claude afterwards,
so prefer letting a borderline role through over filtering it out here.
"""

# ---------------------------------------------------------------------------
# JSearch (Google for Jobs -> LinkedIn, Indeed, Glassdoor, ZipRecruiter, company sites)
#
# Strategy: a few BROAD queries with many pages, then filter locally.
# Each page is ~10 listings. Quota cost per query (per JSearch's docs):
#   num_pages 1      -> 1 request
#   num_pages 2-10   -> 2 requests
#   num_pages 11+    -> 3 requests
# Free BASIC tier = 200 requests/month. Default below ~= 4/day = ~120/month,
# leaving ~80 for manual re-runs. Check usage on your RapidAPI dashboard.
# ---------------------------------------------------------------------------
JSEARCH_URL = "https://jsearch.p.rapidapi.com/search-v2"   # v5 of the API
JSEARCH_DATE_POSTED = "3days"   # today | 3days | week | month | all
                                # "today" is too strict (1-2 Toronto results). Seen-job
                                # tracking means a role is only ever reported once.

JSEARCH_QUERIES = [
    # (query, country code, remote_only, pages)
    # The v2 endpoint returns ~10 listings per call and pages with a cursor.
    # Each page = 1 request. Default: 4 requests/day = ~120/month.
    ("product manager in Toronto, ON", "ca", False, 2),   # GTA on-site/hybrid
    ("remote product manager Canada", "ca", False, 1),    # Canada remote (the work_from_home
                                                          # flag returns worldwide spam)
    ("senior product manager", "us", True, 1),            # US remote (delete to save ~30/month)
]

# ---------------------------------------------------------------------------
# Free sources (no key). Set to False to disable.
# ---------------------------------------------------------------------------
ENABLE_REMOTEOK = True
ENABLE_WWR = True          # We Work Remotely - product category RSS
ENABLE_ADZUNA = True
ENABLE_BUILTIN = True      # Built In Toronto search pages (page 1 only; robots.txt blocks ?page=)

# (url, default location label). daysSinceUpdated=1 keeps each search to one page
# when run daily. Never add &page= - Built In's robots.txt disallows it.
BUILTIN_SEARCHES = [
    ("https://builtintoronto.com/jobs/hybrid/office/product-management/product-leadership"
     "?daysSinceUpdated=1&city=Toronto&state=Ontario&country=CAN&allLocations=true", "Toronto, ON"),
    ("https://builtintoronto.com/jobs/remote/product-management/product-leadership"
     "?daysSinceUpdated=1&country=CAN&allLocations=true", "Canada (Remote)"),
]
BUILTIN_MAX_JOB_PAGES = 25   # job detail pages fetched per run (1s apart)       # only runs if ADZUNA_APP_ID / ADZUNA_APP_KEY secrets exist

ADZUNA_QUERIES = [
    # (what, where) - Canada endpoint
    ("product manager", "Toronto"),
    ("director of product", "Ontario"),
]

# Only keep listings posted within this many hours (applies to all sources).
MAX_AGE_HOURS = 168  # 7 days. JSearch is already limited to "today" by the API; the
                     # free feeds post a few roles a week, and seen-job tracking stops repeats.

# ---------------------------------------------------------------------------
# Title filters (case-insensitive substring match)
# ---------------------------------------------------------------------------
TITLE_INCLUDE = [
    "product manager", "product management", "product lead", "lead product",
    "head of product", "director of product", "director, product", "product director",
    "vp product", "vp of product", "vp, product", "vice president of product",
    "vice president, product", "group product", "principal product", "staff product",
    "chief product", "product leader", "cpo",
]

# Whole-word match, so "engineer" drops "Software Engineer" but keeps
# "Product Manager, Engineering Platform".
TITLE_EXCLUDE = [
    "associate product", "junior", "intern", "internship", "co-op", "coop",
    "new grad", "apm", "product marketing", "product designer", "product design",
    "engineer", "project manager", "program manager", "product owner",
    "product analyst", "product specialist", "product support",
    "product manager i", "product manager 1",
]

# ---------------------------------------------------------------------------
# Location filters
# A job passes if: it's in the GTA/Ontario, OR it's remote and not restricted to
# a region you can't work from.
# ---------------------------------------------------------------------------
GTA_KEYWORDS = [
    "toronto", "mississauga", "markham", "vaughan", "richmond hill", "oakville",
    "brampton", "north york", "scarborough", "etobicoke", "burlington", "pickering",
    "ajax", "whitby", "oshawa", "newmarket", "aurora", "waterloo", "kitchener",
    "ontario", "gta",
]

REMOTE_KEYWORDS = ["remote", "anywhere", "work from home", "distributed"]

# A remote role passes only if its location is one of these (or has no specific
# country). Anything else - "Nigeria (Remote)", "Europe", "India" - is dropped.
REMOTE_ALLOWED_REGIONS = [
    "canada", "united states", "usa", "u.s.", "us", "north america", "americas",
    "anywhere", "worldwide", "global",
    "ontario", "quebec", "british columbia", "alberta", "manitoba", "saskatchewan",
    "nova scotia", "new brunswick",
]

# Reposting/spam aggregators that list themselves as the employer
# (matched against the company name, case-insensitive substring).
# Real employers posted *via* job sites (e.g. Palo Alto Networks on Himalayas) are kept.
EXCLUDE_COMPANIES = [
    "remote quest jobs", "jzone", "jobshives", "wfhsprint", "remotical", "jobgether",
    "remotepromsp",
]

# State file pruning: forget job IDs older than this many days.
SEEN_RETENTION_DAYS = 60
