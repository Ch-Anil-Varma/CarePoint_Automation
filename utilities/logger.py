import logging
import os

def get_logger(name=__name__):
    report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(report_dir, exist_ok=True)

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(os.path.join(report_dir, "execution.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - [%(name)s] - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger