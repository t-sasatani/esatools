import logging
import os
from dotenv import load_dotenv
from datetime import datetime

import coloredlogs
load_dotenv()

log_level = os.environ.get("ESATOOLS_LOG_LEVEL", "INFO")
class EsaUtilLogger:
    """
    Custom logger class to add line numbers to log messages with a level of WARNING or higher.
    """

    def __init__(
        self, level=log_level, fmt=None, log_file=None, log_dir="log"
    ):
        """
        Construct the LoRaDAQLogger class.

        Parameters
        ----------
        level : str
            The logging level for the console.
        fmt : str
            The format for the log messages.
        log_file : str
            The name of the log file.
        log_dir : str
            The directory for the log file.

        """
        if fmt is None:
            fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

        self.level = level
        self.fmt = fmt
        self.log_dir = log_dir

        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)

        if log_file is None:
            start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = f"{start_time}.log"

        self.log_file = os.path.join(log_dir, log_file)

    class LineNumberFilter(logging.Filter):
        """
        Custom filter class to add line numbers.
        """

        def filter(self, record) -> bool:
            """
            Add line numbers to log messages with a level of WARNING or higher.

            Parameters
            ----------
            record : LogRecord
                The log record.

            Returns
            -------
            bool
                True if the log message is at least WARNING level, False otherwise.

            """
            if record.levelno >= logging.WARNING:
                record.msg = f"{record.msg} ({record.filename}:{record.lineno})"
            return True

    def get_logger(self, name):
        """
        Create and configure a logger with the provided name.

        Args:
            name (str): The name for the logger, typically use __name__ from the calling module.

        Returns:
            logging.Logger: Configured logger instance.

        """
        # Create a logger with the provided name
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        # Console logging with colored logs
        coloredlogs.install(level=self.level, logger=logger, fmt=self.fmt)

        # Line number filter instance
        line_number_filter = self.LineNumberFilter()

        # Add file handler with DEBUG level
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(
            logging.DEBUG
        )  # Ensure all messages are logged in the file
        file_handler.setFormatter(logging.Formatter(self.fmt))
        file_handler.addFilter(line_number_filter)
        logger.addHandler(file_handler)

        return logger
