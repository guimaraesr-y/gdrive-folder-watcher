# 🗃️ Google Drive Folder Watcher

Monitor a Google Drive folder for new files and send an email notification.

## 💡 Features

- Automatically detects new files in a Google Drive folder.
- Sends an email notification to specified recipients whenever a new file is detected.
- Downloads the new file from Google Drive and saves it locally (can delete local file after handling).
- Supports multiple email notification handlers.

## 🔧 Installation

### ⚠️ Prerequisites

- Python 3.10 or later
- A Google Cloud Platform project with the Drive API enabled
- A service account key file (credentials.json)

### Setup

1. Clone this repository:

```bash
$ git clone https://github.com/ryangregorydev/google-drive-folder-monitor.git
```

2. Install the required Python packages using pip:
   
```bash
$ pip install -r requirements.txt
```

3. Create a new project and a new service account key file in Google Cloud Platform (GCP) and store it somewhere on your disk.

4. Create and configure you `.env` file:

```bash
$ touch .env

# .env file example content
CREDENTIALS_FILE=<path to your service account key file>
DRIVE_FOLDER_ID=<your Google Drive folder ID>
POLL_INTERVAL=60

GMAIL_EMAIL=example@gmail.com
GMAIL_PASSWORD=xxxxxxxxxx

EMAIL_TO=targetemail@example.com,targetemail2@example.com
```

> If you have MFA activated on your Google account, you will need to create a app password and add it to your .env file.

5. Run the script:

```bash
$ python main.py
```