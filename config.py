import os

# Root directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder and file paths
DB_PATH      = os.path.join(BASE_DIR, "database", "expenses.db")
LOG_PATH     = os.path.join(BASE_DIR, "logs",    "app.log")
HISTORY_PATH = os.path.join(BASE_DIR, "history", "history.txt")
EXPORTS_DIR  = os.path.join(BASE_DIR, "exports")
CHARTS_DIR   = os.path.join(BASE_DIR, "charts")
BANNER_PATH  = os.path.join(BASE_DIR, "assets",  "banner.txt")