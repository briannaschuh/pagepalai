import logging

def setup_logger(name=__name__, log_file=None):
    """
    Sets up and returns a logger with stream and optional file output.

    Args:
        name (str, optional): Name of the logger (default is module name).
        log_file (str, optional): If provided, logs will also be written to this file.

    Returns:
        logging.Logger: Configured logger instance.
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        handlers=handlers
    )
    return logging.getLogger(name)
