# utils/logger.py
import logging
from pathlib import Path

def get_logger(name: str = "pipeline"):
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(name)