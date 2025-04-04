import time
import logging
from src.logging_config import setup_logging


def test_setup_logging_creates_log_file(tmp_path):
    log_path = tmp_path / "test.log"
    
    setup_logging(str(log_path), level=logging.INFO)

    logger = logging.getLogger()

    logger.info("Das ist ein Testeintrag.")

    for handler in logger.handlers:
        handler.flush()

    time.sleep(0.1) 

    assert log_path.exists(), "Log-Datei wurde nicht erstellt."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Das ist ein Testeintrag." in content
