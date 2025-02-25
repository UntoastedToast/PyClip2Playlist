import logging
import sys

def configure_logger() -> None:
    """Konfiguriere das Logging für die Anwendung."""
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
