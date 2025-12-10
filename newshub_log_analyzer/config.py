# Configuration pour Newsroom Googlebot Log Analyzer

# Fichier source (access.log)
LOG_FILE = "access.log"

# Répertoire de sortie
OUTPUT_DIR = "reports"

# Nombre de top URLs à afficher
TOP_URLS_COUNT = 20

# Patterns pour détecter les pages obsolètes
OBSOLETE_PATTERNS = [
    "/archive/",
    "/old/",
    "/deprecated/",
    "/legacy/",
    "old-content",
    "obsolete"
]

# Configuration logging
LOG_ENCODING = "utf-8"
LOG_ERRORS = "ignore"  # ou "strict"

# Plotly configuration
PLOTLY_THEME = "plotly"  # ou "plotly_dark"
PLOTLY_HEIGHT = 1800
PLOTLY_RESPONSIVE = True

# CSV Export
CSV_COLUMNS = [
    'url',
    'crawl_count',
    'status_codes',
    'avg_size',
    'depth',
    'first_crawl',
    'last_crawl',
    'error_count',
    'error_rate',
    'is_obsolete'
]

# Dashboard Visualization Config
DASHBOARD_CONFIG = {
    "timeline": {
        "title": "📈 Crawls Timeline (Daily & Hourly)",
        "type": "line"
    },
    "top_urls": {
        "title": "🔝 Top URLs Crawled",
        "type": "bar",
        "limit": 20
    },
    "errors": {
        "title": "⚠️ HTTP Status Codes",
        "type": "pie"
    },
    "depth": {
        "title": "📊 URL Depth Distribution",
        "type": "histogram"
    },
    "obsolete": {
        "title": "🗑️ Obsolete Pages Analysis",
        "type": "scatter"
    }
}

# Date/Time Parsing
DATE_FORMAT = "%d/%b/%Y:%H:%M:%S"
TIMEZONE = "+0000"

# Googlebot Detection
GOOGLEBOT_PATTERNS = [
    "googlebot",
    "bingbot",
    "slurp",
    "duckduckgo",
    "baiduspider",
    "yandexbot"
]

# Performance Optimization
CHUNK_SIZE = 50000  # Process logs in chunks for large files
VERBOSE = True      # Print progress messages

# KPI Thresholds
ERROR_RATE_THRESHOLD = 0.2      # Flag URLs with > 20% errors
MIN_CRAWL_COUNT_THRESHOLD = 5   # Only analyze URLs with 5+ crawls
MAX_DEPTH_THRESHOLD = 10        # Flag URLs deeper than 10 levels
