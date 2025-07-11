# file for logging
import logging
import logging.handlers
import sys
import os

# class for logger
class Logger:
    """
    Logger supporting multiple levels, console and file handlers, log rotation, and configurable formats.
    """
    def __init__(self, name:str, log_file:str, level:int=logging.DEBUG, max_bytes:int=10*1024*1024, 
                 backup_count:int=5, fmt:str='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 datefmt:str='%Y-%m-%d %H:%M:%S', console:bool=True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        
        # formatter
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        
        # console message
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
        if log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
        
    def log_debug(self, message:str, **kwargs):
        try:
            self.logger.debug(message, **kwargs)
        except Exception as e:
            sys.stderr.write(f"Logging debug failed: {e}\n")
            
    def log_info(self, message:str, **kwargs):
        try:
            self.logger.info(message, **kwargs)
        except Exception as e:
            sys.stderr.write(f"Logging info failed: {e}\n")
            
    def log_warning(self, message:str, **kwargs):
        try:
            self.logger.warning(message, **kwargs)
        except Exception as e:
            sys.stderr.write(f"Logging warning failed: {e}\n")
            
    def log_error(self, message:str, **kwargs):
        try:
            self.logger.error(message, **kwargs)
        except Exception as e:
            sys.stderr.write(f"Logging error failed: {e}\n")
            
    def log_critical(self, message:str, **kwargs):
        try:
            self.logger.critical(message, **kwargs)
        except Exception as e:
            sys.stderr.write(f"Logging critical failed: {e}\n")
            
    def exception(self, message:str):
        """
        Logs an exception traceback with ERROR level.
        """
        try:
            self.logger.exception(message)
        
        except Exception as e:
            sys.stderr.write(f"Logging exception failed: {e}\n")
        

# initialize the logger
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "logs.txt")
logger = Logger("Research_Assistant", log_file)
            
            
