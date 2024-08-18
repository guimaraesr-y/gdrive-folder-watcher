import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_FILE = os.environ.get("CREDENTIALS_FILE")
DRIVE_FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID")
SCOPES = ["https://www.googleapis.com/auth/drive"]

# interval in seconds for polling
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL")) or 60  

# gmail credetials
APP_EMAIL = os.environ.get("GMAIL_EMAIL")
APP_PASSWORD = os.environ.get("GMAIL_PASSWORD")

# email recipients
EMAIL_TO = os.environ.get("EMAIL_TO").split(",")