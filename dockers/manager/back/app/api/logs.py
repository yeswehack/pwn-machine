import sqlite3
from app.config import PM_LOG_FILE
logdb = sqlite3.connect(PM_LOG_FILE)
