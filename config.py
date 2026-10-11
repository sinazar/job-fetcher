"""
Search settings for the daily fetcher. Edit this file to change what gets pulled.

The fetcher is deliberately "dumb": it casts a reasonably wide net using cheap
keyword rules. Fit scoring, judgment and the digest happen in Claude afterwards,
so prefer letting a borderline role through over filtering it out here.
"""

# ---------------------------------------------------------------------------
# JSearch (Google for Jobs -> LinkedIn, Indeed, Glassdoor, ZipRecruiter, company sites)
# Each entry = 1 API request per run (with num_pages=1).
# Free BASIC tier is 200 requests/month -> 4 queries x 30 days = 120/month.
# ---------------------------------------------------------------------------
JSEARCH_DATE_POSTED = "today"   # today | 3days | week | month | all
JSEARCH_NUM_PAGES = 1           # >1 returns more results but can cost extra quota

JSEARCH_QUERIES = [
    # (query, country code, remote_only)
    ("senior product manager in Toronto, Ontario", "ca", False),
    ("director of product OR head of product OR principal product manager in Toronto, Ontario", "ca", False),
    ("senior product manager AI", "ca", True),
    ("principal OR group OR senior product manager AI platform", "us", True),
]

# ---------------------------------------------------------------------------
# Free sources (no key). Set to False to disable.
# ---------------------------------------------------------------------------
ENABLE_REMOTEOK = True
ENABLE_WWR = True          # We Work Remotely - product category RSS
ENABLE_ADZUNA = True       # only runs if ADZUNA_APP_ID / ADZUNA_APP_KEY secrets exist

ADZUNA_QUERIES = [
    # (what, where) - Canada endpoint
    ("product manager", "Toronto"),
    ("director of product", "Ontario"),
]

# Only keep listings posted within this many hours (applies to all sources).
MAX_AGE_HOURS = 30   # a little over 24h so a late GitHub cron run doesn't drop anything

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

# Remote roles restricted to these regions are dropped.
REMOTE_EXCLUDE_REGIONS = [
    "europe", "emea", "uk only", "united kingdom", "germany", "france", "spain",
    "netherlands", "poland", "portugal", "ireland", "india", "apac", "asia",
    "australia", "new zealand", "latam", "latin america", "brazil", "mexico",
    "argentina", "philippines", "singapore", "japan", "africa", "israel",
]

# State file pruning: forget job IDs older than this many days.
SEEN_RETENTION_DAYS = 60
