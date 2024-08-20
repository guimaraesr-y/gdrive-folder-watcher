import pathlib
from typing import List


class PersistenceService:
    def __init__(self, storage_path: pathlib.Path = pathlib.Path("./data.txt")):
        self.storage_path = storage_path
        self.storage_path.touch(exist_ok=True)

        self.data = self.read_data()

    def read_data(self) -> List[str]:
        """
        Reads data from the storage path.

        Returns:
            dict: The data read from the storage path.
        """
        with open(self.storage_path, "r") as f:
            return map(lambda x: x.strip(), f.readlines())

    def write_data(self, data: dict) -> None:
        """
        Writes (and overwrites) data to the storage path and updates the internal data attribute.

        Args:
            data (dict): The data to be written to the storage path.

        Returns:
            None
        """
        with open(self.storage_path, "w") as f:
            f.write(data)

        self.data = data
