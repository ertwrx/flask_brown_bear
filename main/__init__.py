from flask import Flask
from .config import get_config
import os
import signal
import threading

# Optional: global event used by any thread-based services
shutdown_event = threading.Event()

def handle_shutdown(signum, frame):
    print(f"Received shutdown signal: {signum}")
    shutdown_event.set()

# Register signal handlers globally at import time
signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

def create_app(config_class=None):
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    if config_class is None:
        app.config.from_object(get_config())
    else:
        app.config.from_object(config_class)

    with app.app_context():
        from .routes import register_routes
        register_routes(app)

        # If you start any long-lived threads, pass shutdown_event to them

    return app
