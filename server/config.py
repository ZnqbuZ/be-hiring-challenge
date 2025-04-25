import logging
from logging import config
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    API_ROOT = os.environ.get("API_ROOT", "/")
    SERIALIZER = os.environ.get("SERIALIZER", "parquet")
    WORKER_ENDPOINT = os.environ.get("WORKER_ENDPOINT", "http://dataset-worker")
    FILE_STORE = Path(os.environ.get("FILE_STORE", "/var/lib/app"))


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # 保留已有的日志器
    "formatters": {
        "default": {
            "()" : "colorlog.ColoredFormatter",
            "format": "[%(asctime)s] %(log_color)s[%(levelname)s]\t\033[0m[%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG":    "cyan",
                "INFO":     "green",
                "WARNING":  "yellow",
                "ERROR":    "red",
                "CRITICAL": "bold_red",
            }
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
