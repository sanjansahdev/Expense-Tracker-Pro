import logging
import os
from datetime import datetime
from config import LOG_PATH, BANNER_PATH, HISTORY_PATH

# Ensure logs and history directories exist
os.makedirs(os.path.dirname(LOG_PATH),     exist_ok=True)
os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_action(message):
    """Logs user actions into app.log."""
    logging.info(message)

def write_history(action, details=""):
    """Appends a human-readable entry to history/history.txt."""
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    line = f"[{timestamp}]  {action:<22}  |  {details}\n"
    with open(HISTORY_PATH, "a", encoding="utf-8") as f:
        f.write(line)

def print_banner():
    """Prints the ASCII art banner if available."""
    if os.path.exists(BANNER_PATH):
        with open(BANNER_PATH, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("=== EXPENSE TRACKER PRO ===")