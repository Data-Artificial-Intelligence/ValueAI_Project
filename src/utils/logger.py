"""Standardized logging for the ValueAI project."""
import logging
import sys
from pathlib import Path


def get_logger(name: str, log_file: str = "valueai.log") -> logging.Logger:
    """Create a logger that outputs to both console and file."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    log_dir = Path(__file__).parents[2] / "logs"
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger