from typing import List
from config import *
from lib.drive.drive_service import DriveService
from lib.drive.file_event_handler_wrapper import FileEventHandlerWrapper
from lib.drive.folder_poller import FolderPoller
from lib.emailing.gmail_event_handler import GmailEventHandler
from lib.emailing.gmail_service import GmailService


class App:
    def __init__(
        self,
        credentials_file: str,
        folder_id: str,
        poll_interval: int,
        to_email: List[str],
    ):
        self.drive_service = DriveService(credentials_file, SCOPES)

        gmail_service = GmailService(APP_EMAIL, APP_PASSWORD)
        self.gmail_handler = GmailEventHandler(
            gmail_service=gmail_service, to_email=to_email
        )

        self.event_handler = FileEventHandlerWrapper(
            drive_service=self.drive_service,
            handlers=[self.gmail_handler],
            delete_local_file_after_handled=True,
        )
        self.folder_poller = FolderPoller(
            self.drive_service, folder_id, self.event_handler, poll_interval
        )

    def run(self):
        self.folder_poller.poll()


if __name__ == "__main__":
    app = App(
        credentials_file=CREDENTIALS_FILE,
        folder_id=DRIVE_FOLDER_ID,
        poll_interval=POLL_INTERVAL,
        to_email=EMAIL_TO,
    )

    app.run()
