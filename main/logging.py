import logging
import sys

def configure_logging(app):
    """Configure logging for the application."""
    # Clear existing handlers
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
    
    # Set log level from config
    log_level_name = app.config.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)
    app.logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    # Log successful configuration
    app.logger.info(f"Logging configured with level: {log_level_name}")
