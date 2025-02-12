import logging
import os

class EsaUtilLogger:
    def __init__(self, name=__name__, log_file='app.log'):
        # Create a custom logger
        self.logger = logging.getLogger(name)
        
        # Define the log level, defaulting to INFO, configurable via environment variable
        log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Only add handlers if they haven't been added already
        if not self.logger.hasHandlers():
            # Create handlers
            console_handler = logging.StreamHandler()
            file_handler = logging.FileHandler(log_file)
            
            # Set levels for handlers
            console_handler.setLevel(logging.INFO)
            file_handler.setLevel(logging.DEBUG)

            # Create formatters and add them to the handlers
            log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(log_format)
            file_handler.setFormatter(log_format)

            # Add handlers to the logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def get_logger(self):
        return self.logger