import pathlib
from typing import List
from lib.drive.file_event_handler_wrapper import EventHandler
from lib.emailing.gmail_service import GmailService


class GmailEventHandler(EventHandler):
    def __init__(self, gmail_service: GmailService, to_email: List[str]):
        self.gmail_service = gmail_service
        self.to_email = to_email

    def on_new_file_detected(self, file: dict, file_path: pathlib.Path):
        print(f"[+] Emailing {', '.join(self.to_email)}")

        for email in self.to_email:
            self.gmail_service.send_message(
                to=email,
                subject="New file detected!",
                message_text=f"A new file {file_path.name} was detected in your Google Drive. Please check.",
                files=[file_path.absolute()],
            )
