from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class DriveService:
    def __init__(self, credentials_file: str, scopes: list):
        self.credentials_file = credentials_file
        self.scopes = scopes
        self.service = self.authenticate_drive_api()

    def authenticate_drive_api(self):
        """
        Authenticates with the Google Drive API using service account credentials.

        Args:
            None

        Returns:
            googleapiclient.discovery.Resource: A Google Drive API client instance.
        """
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=self.scopes
        )

        return build("drive", "v3", credentials=credentials)

    def list_files_in_folder(self, folder_id: str) -> list:
        """
        Lists files inside a Google Drive folder.

        Args:
            folder_id (str): The ID of the folder to list files from.

        Returns:
            list: A list of dictionaries where each dictionary contains the
                'id' and 'name' of a file inside the folder.
        """
        query = f"'{folder_id}' in parents and trashed = false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        return results.get("files", [])

    def download_file_by_id(self, file_id, local_path):
        """
        Downloads a file from Google Drive by its ID and saves it to a local path.

        Args:
            file_id (str): The ID of the file to download.
            local_path (str): The path where the file will be saved.

        Returns:
            None
        """
        request = self.service.files().get_media(fileId=file_id)
        with open(local_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100), end="\r")
            print()
