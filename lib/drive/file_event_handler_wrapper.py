import pathlib
from typing import List

from abc import ABC, abstractmethod

from lib.drive.drive_service import DriveService


class EventHandler(ABC):
    
    @abstractmethod
    def on_new_file_detected(self, file: dict, file_path: pathlib.Path) -> None:
        pass
    

class FileEventHandlerWrapper(EventHandler):

    def __init__(
        self,
        drive_service: DriveService,
        handlers: List[EventHandler] = [],
        delete_local_file_after_handled=False,
    ):
        self.drive_service = drive_service
        self.handlers = [*handlers]
        self.delete_local_file_after_handled = delete_local_file_after_handled

    def on_new_file_detected(self, file: dict) -> None:
        """
        Handles the detection of a new file in the Google Drive folder.

        Args:
            file (dict): A dictionary containing the 'id' and 'name' of the new file.

        Returns:
            None
        """
        file_name = file.get("name")
        file_id = file.get("id")

        # creates the download directory if it doesn't exist
        download_dir = pathlib.Path("./downloads")
        download_dir.mkdir(parents=True, exist_ok=True)
        download_path = download_dir / file.get("name")

        print(f"New file detected: {file_name} (ID: {file_id})")

        # downloads the file
        self.drive_service.download_file_by_id(file_id, download_path)
        
        # calls the handlers
        for handler in self.handlers:
            handler.on_new_file_detected(file, download_path)

        # deletes the file if needed
        if self.delete_local_file_after_handled:
            pathlib.Path(download_path).unlink()
