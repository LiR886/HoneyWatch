import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import get_settings


settings = get_settings()


def build_logger(name: str, filename: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    log_path = Path(settings.log_dir) / filename
    handler = RotatingFileHandler(
        log_path,
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


event_logger = build_logger("honeywatch.events", "honeypot.log")
alert_logger = build_logger("honeywatch.alerts", "alerts.log")
