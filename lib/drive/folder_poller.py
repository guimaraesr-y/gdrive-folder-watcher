import time

from lib.drive.drive_service import DriveService
from lib.drive.file_event_handler_wrapper import FileEventHandlerWrapper
from lib.persistence.persistence_service import PersistenceService


class FolderPoller:
    def __init__(
        self,
        drive_service: DriveService,
        folder_id: str,
        event_handler: FileEventHandlerWrapper,
        persistence_service: PersistenceService,
        poll_interval: int,
    ):
        self.drive_service = drive_service
        self.folder_id = folder_id
        self.event_handler = event_handler
        self.persistence_service = persistence_service
        self.poll_interval = poll_interval
        self.known_files = set(self.persistence_service.read_data())

    def poll(self):
        """
        Polls the Google Drive folder for new files at regular intervals.

        Continuously checks the folder for new files and triggers the event handler
        when a new file is detected. The polling interval is determined by the
        `poll_interval` attribute of the `FolderPoller` instance.

        Args:
            None

        Returns:
            None
        """
        print("[+] Polling...")

        while True:
            try:
                # list all files in the folder
                current_files = self.drive_service.list_files_in_folder(self.folder_id)
            except Exception as e:
                print(f"Error listing files in folder: {e}")
                time.sleep(self.poll_interval)
                continue
            
            current_file_ids = {file["id"] for file in current_files}
            
            # persists the list of known files
            self.persistence_service.write_data('\n'.join(current_file_ids))

            # detected new files
            new_files = [
                file for file in current_files if file["id"] not in self.known_files
            ]

            # trigger the event handler
            for new_file in new_files:
                self.event_handler.on_new_file_detected(new_file)

            # update the list of known files
            self.known_files = current_file_ids

            # wait for the polling interval
            time.sleep(self.poll_interval)
