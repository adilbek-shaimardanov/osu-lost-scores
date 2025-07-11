import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from path_utils import get_env_path, get_standard_dir, mask_path_for_log

logger = logging.getLogger(__name__)
DEFAULT_ENV_CONTENT = """# Analysis Configuration
CUTOFF_DATE=1730114220

# Logging Configuration
LOG_LEVEL=DEBUG
LOG_DIR=log

# Database Configuration
DB_FILE=beatmap_info.db

# Path Settings
CACHE_DIR=cache
RESULTS_DIR=results
MAPS_DIR=maps
CSV_DIR=csv

# Performance Configuration
GUI_THREAD_POOL_SIZE=24   # For QThreadPool in GUI module
THREAD_POOL_SIZE=16       # For ThreadPoolExecutor in file_parser.py
IO_THREAD_POOL_SIZE=32    # For I/O operations in analyzer.py

# Download Configuration
MAP_DOWNLOAD_TIMEOUT=30
DOWNLOAD_RETRY_COUNT=3
CHECK_MISSING_BEATMAP_IDS=False

# API Configuration
API_RETRY_COUNT=3
API_RETRY_DELAY=0.5
API_REQUESTS_PER_MINUTE=60
# WARNING: peppy prohibits using more than 60 requests per minute
# Burst spikes up to 1200 requests per minute are possible, but proceed at your own risk
# It may result in API/website usage ban
# More than 1200 requests per minute will not work (upper limit)
"""
PUBLIC_REQUESTS_PER_MINUTE = 1200
dotenv_path_str_from_env_var = os.environ.get("DOTENV_PATH")
if dotenv_path_str_from_env_var and os.path.exists(dotenv_path_str_from_env_var):
    dotenv_path = Path(dotenv_path_str_from_env_var)
else:
    dotenv_path = Path(get_env_path())
if not dotenv_path.exists():
    try:
        dotenv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dotenv_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_ENV_CONTENT)
        logger.info(
            f"Default .env file created at {mask_path_for_log(str(dotenv_path))}"
        )
    except (IOError, OSError):
        logger.exception(
            "Failed to create default .env file at %s", mask_path_for_log(str(dotenv_path))
        )
if dotenv_path.exists():
    logger.info("Loading .env from: %s", mask_path_for_log(str(dotenv_path)))
    load_dotenv(dotenv_path=dotenv_path, override=True)
else:
    logger.error(
        "Could not find .env file: %s (even after attempting creation)",
        mask_path_for_log(str(dotenv_path)),
    )
_cache_dir_name = os.environ.get("CACHE_DIR", "cache")
_results_dir_name = os.environ.get("RESULTS_DIR", "results")
_maps_dir_name = os.environ.get("MAPS_DIR", "maps")
_csv_dir_name = os.environ.get("CSV_DIR", "csv")
_log_dir_name = os.environ.get("LOG_DIR", "log")
_log_level_name = os.environ.get("LOG_LEVEL", "INFO")

CACHE_DIR = get_standard_dir(_cache_dir_name)
RESULTS_DIR = get_standard_dir(_results_dir_name)
MAPS_DIR = get_standard_dir(_maps_dir_name)
CSV_DIR = get_standard_dir(_csv_dir_name)
LOG_DIR = get_standard_dir(_log_dir_name)

AVATAR_DIR = os.path.join(CACHE_DIR, "avatars")
COVER_DIR = os.path.join(CACHE_DIR, "covers")

LOG_LEVEL = _log_level_name

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(MAPS_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(AVATAR_DIR, exist_ok=True)
os.makedirs(COVER_DIR, exist_ok=True)

_db_filename = os.environ.get("DB_FILE", "beatmap_info.db")
DB_FILE = os.path.join(CACHE_DIR, _db_filename)

cutoff_env = os.environ.get("CUTOFF_DATE", "1730114220")
try:
    CUTOFF_DATE = int(cutoff_env)
except ValueError:
    logger.warning(
        "Could not convert CUTOFF_DATE '%s' to number, using default value", cutoff_env
    )
    CUTOFF_DATE = 1730114220
thread_pool_env = os.environ.get("THREAD_POOL_SIZE", "16")
try:
    THREAD_POOL_SIZE = int(thread_pool_env)
except ValueError:
    logger.warning(
        "Could not convert THREAD_POOL_SIZE '%s' to number, using default value",
        thread_pool_env,
    )
    THREAD_POOL_SIZE = 16
io_thread_pool_env = os.environ.get(
    "IO_THREAD_POOL_SIZE", str((os.cpu_count() or 16) * 2)
)
try:
    IO_THREAD_POOL_SIZE = int(io_thread_pool_env)
except ValueError:
    logger.warning(
        "Could not convert IO_THREAD_POOL_SIZE '%s' to number, using default value",
        io_thread_pool_env,
    )
    IO_THREAD_POOL_SIZE = min(32, (os.cpu_count() or 8) * 2)
gui_thread_pool_env = os.environ.get("GUI_THREAD_POOL_SIZE", "24")
try:
    GUI_THREAD_POOL_SIZE = int(gui_thread_pool_env)
except ValueError:
    logger.warning(
        "Could not convert GUI_THREAD_POOL_SIZE '%s' to number, using default value",
        gui_thread_pool_env,
    )
    GUI_THREAD_POOL_SIZE = 24
map_download_timeout_env = os.environ.get("MAP_DOWNLOAD_TIMEOUT", "30")
try:
    MAP_DOWNLOAD_TIMEOUT = int(map_download_timeout_env)
except ValueError:
    logger.warning(
        "Could not convert MAP_DOWNLOAD_TIMEOUT '%s' to number, using default value",
        map_download_timeout_env,
    )
    MAP_DOWNLOAD_TIMEOUT = 30
download_retry_count_env = os.environ.get("DOWNLOAD_RETRY_COUNT", "3")
try:
    DOWNLOAD_RETRY_COUNT = int(download_retry_count_env)
except ValueError:
    logger.warning(
        "Could not convert DOWNLOAD_RETRY_COUNT '%s' to number, using default value",
        download_retry_count_env,
    )
    DOWNLOAD_RETRY_COUNT = 3
check_missing_ids_env = os.environ.get("CHECK_MISSING_BEATMAP_IDS", "False").lower()
CHECK_MISSING_BEATMAP_IDS = check_missing_ids_env in ("true", "1", "yes")
api_requests_per_minute_env = os.environ.get("API_REQUESTS_PER_MINUTE", "60")
api_retry_count_env = os.environ.get("API_RETRY_COUNT", "3")
api_retry_delay_env = os.environ.get("API_RETRY_DELAY", "0.5")
try:
    API_REQUESTS_PER_MINUTE = int(api_requests_per_minute_env)
    if API_REQUESTS_PER_MINUTE <= 0:
        logger.warning(
            "API_REQUESTS_PER_MINUTE set to %d, treating as unlimited. This is dangerous!",
            API_REQUESTS_PER_MINUTE,
        )
        API_RATE_LIMIT = 0.0
    else:
        API_RATE_LIMIT = 60.0 / API_REQUESTS_PER_MINUTE
except ValueError:
    logger.warning(
        "Could not convert API_REQUESTS_PER_MINUTE '%s' to number, using default value",
        api_requests_per_minute_env,
    )
    API_REQUESTS_PER_MINUTE = 60
    API_RATE_LIMIT = 1.0
try:
    API_RETRY_COUNT = int(api_retry_count_env)
except ValueError:
    logger.warning(
        "Could not convert API_RETRY_COUNT '%s' to number, using default value",
        api_retry_count_env,
    )
    API_RETRY_COUNT = 3
try:
    API_RETRY_DELAY = float(api_retry_delay_env)
except ValueError:
    logger.warning(
        "Could not convert API_RETRY_DELAY '%s' to number, using default value",
        api_retry_delay_env,
    )
    API_RETRY_DELAY = 0.5
OSU_API_LOG_LEVEL = os.environ.get("OSU_API_LOG_LEVEL", "INFO")
logger.info(
    "Configured API settings: API_REQUESTS_PER_MINUTE=%d, API_RETRY_COUNT=%s, API_RETRY_DELAY=%s, OSU_API_LOG_LEVEL=%s",
    API_REQUESTS_PER_MINUTE,
    API_RETRY_COUNT,
    API_RETRY_DELAY,
    OSU_API_LOG_LEVEL,
)
