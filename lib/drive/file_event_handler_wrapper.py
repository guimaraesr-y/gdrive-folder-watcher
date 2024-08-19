import pathlib
from queue import Queue
from threading import Thread
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
        
        self.producer_queue = Queue()
        self.consumer_queue = Queue()
        self.running = True
        
        # Start the consumer and producer threads
        self.producer_thread = Thread(
            target=self.__produce_file_event,
            daemon=True
        )
        self.consumer_thread = Thread(
            target=self.__consume_file_event,
            daemon=True
        )
        
        self.producer_thread.start()
        self.consumer_thread.start()

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

        self.producer_queue.put((file, download_path))
        
    def stop(self):
        """Method to stop the producer and consumer threads"""
        self.running = False
        self.producer_thread.join()
        self.consumer_thread.join()

    def __produce_file_event(self) -> None:
        while self.running:
            file, download_path = self.producer_queue.get()
            self.drive_service.download_file_by_id(file.get("id"), download_path)

            self.consumer_queue.put((file, download_path))            
            self.producer_queue.task_done()

    def __consume_file_event(self) -> None:
        while self.running:
            file, download_path = self.consumer_queue.get()

            for handler in self.handlers:
                handler.on_new_file_detected(file, download_path)

            if self.delete_local_file_after_handled:
                pathlib.Path(download_path).unlink()
            
            self.consumer_queue.task_done()
            