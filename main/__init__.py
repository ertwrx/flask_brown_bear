from flask import Flask
from .config import get_config
import os
import signal
import threading
import sys

# Optional: global event used by any thread-based services
shutdown_event = threading.Event()

# Only register signal handlers when this module is the main program
def register_signal_handlers():
    def handle_shutdown(signum, frame):
        print(f"Received shutdown signal: {signum}")
        shutdown_event.set()
        # Give threads a moment to clean up
        sys.exit(0)
    
    # Only register signal handlers in the main process
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        signal.signal(signal.SIGTERM, handle_shutdown)
        signal.signal(signal.SIGINT, handle_shutdown)

def create_app(config_class=None):
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

  # Register CLI commands for administrative tasks
    from .cli import register_commands
    register_commands(app)

    
    # Apply configuration
    if config_class is None:
        app.config.from_object(get_config())
    else:
        app.config.from_object(config_class)
    
    # Configure logging early
    from .logging import configure_logging
    configure_logging(app)
    
    # Register signal handlers if running directly
    if __name__ == '__main__':
        register_signal_handlers()
    
    with app.app_context():
        from .routes import register_routes
        register_routes(app)
    
    app.logger.info("Application created and configured")
    return app

# Explicitly export the register_signal_handlers function
__all__ = ['create_app', 'register_signal_handlers', 'shutdown_event']
