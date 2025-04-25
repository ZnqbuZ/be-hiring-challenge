import logging
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    API_ROOT = os.environ.get("API_ROOT", "/")
    SERIALIZER = os.environ.get("SERIALIZER", "parquet")
    WORKER_ENDPOINT = os.environ.get("WORKER_ENDPOINT", "http://dataset-worker")
    FILE_STORE = Path(os.environ.get("FILE_STORE", "/var/lib/app"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")
