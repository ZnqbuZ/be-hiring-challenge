import uuid
from collections import UserDict
from contextlib import contextmanager
from enum import Enum
from io import IOBase
from typing import Optional, Generator, IO, List

import pandas as pd

class Dataset:
    """
    A class representing a dataset.
    :param id: id of the dataset (UUID)
    :param name: name of the dataset
    :param data: the dataset as a pandas dataframe
    :param size: size of the dataset
    """

    class Stream(Enum):
        DATA = "data.bin"
        METADATA = "metadata.json"
        EXCEL = "excel.xlsx"
        PLOT = "plot.pdf"

    @contextmanager
    def s_open(self, stream: Stream, mode: str = "rb") -> Generator[IO, None, None]:
        """
        Open the file in the given mode.
        :param stream: The stream to open
        :param mode: The mode to open the file in
        :return: The file object
        """

    _id: uuid.UUID

    _data: Optional[pd.DataFrame]
    _metadata: Optional[UserDict[str, str]]

    @property
    def id(self) -> uuid.UUID:
        """
        Get the id of the dataset.
        :return: The id of the dataset
        """

        return self._id

    @property
    def metadata(self) -> UserDict[str, str]:
        """
        Get the metadata of the dataset.
        :return: The metadata of the dataset
        """

        return self._metadata

    @property
    def name(self) -> str:
        """
        Get the name of the dataset.
        :return: The name of the dataset
        """

        return self.metadata.get("name", "Unnamed")

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the dataset.
        :param value: The name of the dataset
        :return: None
        """

        self._metadata["name"] = value

    @property
    def data(self) -> pd.DataFrame:
        """
        Get the dataset. If the dataset is not loaded, it will be loaded from the stream.
        :return: The dataset as a pandas dataframe
        """

        return self._data

    @property
    def size(self) -> int:
        """
        Get the size of the dataset.
        :return: The size of the dataset
        """

        return self.data.shape[0]

    @property
    def stats(self) -> pd.DataFrame:
        """
        Get the dataset stats.
        :return: The dataset stats
        """

        return self.data.describe()

    @property
    def info(self) -> dict:
        return {**self.metadata, "size": self.size}

    def __init__(self, data: Optional[pd.DataFrame | IOBase] = None, mode: Optional[str] = "pandas",
                 name: Optional[str] = None,
                 id: Optional[str | uuid.UUID] = None) -> None:

        self._data = self._metadata = None

    def sync(self, target: List["DatasetStream"] = ()) -> None:
        """
        Sync the dataset with the file store.
        :return: None
        """
        self.save(target)
        self.load(target)

    def save(self, target: List["DatasetStream"] = ()) -> None:
        """
        Save the dataset to the file store.
        :return: None
        """

    def load(self, target: List["DatasetStream"] = ()) -> None:
        """
        Load the dataset from the file store.
        :return: None
        """


DatasetStream = Dataset.Stream
