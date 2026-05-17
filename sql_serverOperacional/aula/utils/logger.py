# utils/logger.py

import logging
from pathlib import Path
from datetime import datetime

def setup_logging():
    """Configura logs no console e arquivo."""
    Path("logs").mkdir(exist_ok=True)

    log_file = f"logs/etl_censo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    logging.info("Logging iniciado. Arquivo: %s", log_file)
