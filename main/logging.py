import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """Configure logging for the application according to 12-Factor guidelines."""
    log_level_name = app.config.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level_name)
    
    # Use a structured log format - helps with log aggregation
    log_format = '%(asctime)s [%(process)d] [%(levelname)s] %(name)s: %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Clear existing handlers to avoid duplication
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.setLevel(log_level)
    
    # Always log to stdout/stderr (12-factor compliance)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Configure flask app logger
    app.logger.setLevel(log_level)
    
    # Reduce verbosity of werkzeug in production
    if not app.debug:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    app.logger.info(f"Application logging configured at {log_level_name} level")
    return app

