import json
import uuid
from collections import UserDict
from contextlib import contextmanager
from enum import Enum
from io import IOBase
from typing import Optional, Generator, IO, List, cast, Iterator

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from config import Config, logger


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

        path = Config.FILE_STORE / str(self.id) / stream.value
        f = open(path, mode)
        try:
            yield f
        finally:
            f.close()

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

        if self._metadata is None:
            try:
                with self.s_open(DatasetStream.METADATA, "r") as f:
                    self.import_metadata(json.load(f))
            except FileNotFoundError:
                raise ValueError("No metadata available")

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

        if self._data is None:
            self.load()
        return self._data

    @data.setter
    def data(self, value: pd.DataFrame) -> None:
        """
        Set the dataset and sync it with the file store so that all dependent properties are updated.
        :param value:
        :return: None
        """

        self._data = value
        self.sync([DatasetStream.DATA])

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

        # If id is not None, then the dataset will be loaded from the file store later.
        # All other parameters are ignored.
        if id is not None:
            self._id = uuid.UUID(id)
            return

        if data is None:
            raise ValueError("data is required")

        # Create a new dataset with given data
        self._id = uuid.uuid4()

        self.import_metadata({
            "id": str(self.id),
            "name": name if name is not None else "Unnamed",
        })

        self.import_data(data, mode)

    def import_data(self, data: pd.DataFrame | IOBase, mode: str = "pandas") -> None:
        """
        Import data.
        :param data: The data to import
        :param mode: The mode of the data, can be pandas or csv (default: "pandas")
        :return: None
        """

        if isinstance(data, IOBase):
            data = cast(IO[bytes], data)
            if mode == "csv":
                self.data = pd.read_csv(data)
            else:
                raise ValueError(f"Invalid mode: {mode} for string data")
        elif isinstance(data, pd.DataFrame):
            if mode != "pandas":
                logger.warning(f"Invalid mode: {mode} for dataframe data")
            self.data = data

    def import_metadata(self, metadata: dict) -> None:
        """
        Import metadata.
        :param metadata: The metadata to import
        :return: None
        """

        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a dictionary")

        self._metadata = UserDict()
        self._metadata.__setitem__ = lambda k, v: (
            UserDict.__setitem__(self._metadata, k, v),
            self.sync([DatasetStream.METADATA]),
        )[0]

        self._metadata.data = metadata
        self.sync([DatasetStream.METADATA])

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

        if DatasetStream.DATA in target:
            target.append(DatasetStream.EXCEL)
            target.append(DatasetStream.PLOT)

        if len(target) == 0:
            target = list(DatasetStream)

        # Create the directory if it does not exist
        path = Config.FILE_STORE / str(self.id)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        for item in target:
            with self.s_open(item, "wb+") as f:
                fb = cast(IO[bytes], f)
                match item:
                    case DatasetStream.DATA:
                        self.data.to_parquet(fb, engine="pyarrow", index=False)
                    case DatasetStream.EXCEL:
                        self.data.to_excel(fb, engine="openpyxl", index=False)
                    case DatasetStream.PLOT:
                        with PdfPages(fb) as pdf:
                            for column in self.data.select_dtypes(include=["number"]).columns:
                                fig, ax = plt.subplots()
                                self.data[column].hist(ax=ax)
                                ax.set_title(column)
                                pdf.savefig(fig)
                                plt.close(fig)
                    case DatasetStream.METADATA:
                        fb.write(json.dumps(dict(self._metadata), indent=4).encode("utf-8"))

    def load(self, target: List["DatasetStream"] = ()) -> None:
        """
        Load the dataset from the file store.
        :return: None
        """

        if len(target) == 0:
            target = list(DatasetStream)

        for item in target:
            if item == DatasetStream.DATA:
                with self.s_open(item, "rb") as f:
                    fb = cast(IO[bytes], f)
                    self._data = pd.read_parquet(fb, engine="pyarrow")

            if item == DatasetStream.METADATA:
                with self.s_open(item, "r") as f:
                    self._metadata.data = json.load(f)


DatasetStream = Dataset.Stream
