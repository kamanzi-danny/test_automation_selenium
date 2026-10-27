"""Logging setup: one new, timestamped log file per run, plus console output."""

import logging
import os
from datetime import datetime

from includes import constants


def setup_logger():
    """Create a logger that writes to logs/test_run_<date>_<time>.log.

    Every run gets its own file, so earlier runs are never overwritten.
    Returns the logger and the path of the log file.
    """
    os.makedirs(constants.LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(constants.LOG_DIR, f"test_run_{timestamp}.log")

    logger = logging.getLogger("portfolio_tests")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    # Every entry: timestamp | level | message
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Also show the same entries in the terminal / Docker logs.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger, log_path
