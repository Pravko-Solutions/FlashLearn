import logging
import sys

def setup_logger(name="FlashLearn", level=logging.ERROR):
    """
    Sets up a logger with the specified name and level
    and also configures openai, httpx, and httpcore loggers to ERROR.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Silence 3rd-party libraries
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("httpcore").setLevel(logging.ERROR)

    # Only add a StreamHandler if none exist
    if not logger.hasHandlers():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger