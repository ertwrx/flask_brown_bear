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
    
    # Apply configuration
    if config_class is None:
        app.config.from_object(get_config())
    else:
        app.config.from_object(config_class)
    
    with app.app_context():
        from .routes import register_routes
        register_routes(app)
        # If you start any long-lived threads, pass shutdown_event to them
    
    return app

# Explicitly export the register_signal_handlers function
__all__ = ['create_app', 'register_signal_handlers', 'shutdown_event']
