import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("RPA_Suite")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formato de logs
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Handler de Consola
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Handler de Archivo
        fh = logging.FileHandler("logs/execution.log", encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger