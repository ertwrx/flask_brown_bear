import os
from main import create_app
from main import register_signal_handlers  # Add this import

app = create_app()

if __name__ == '__main__':
    # Register signal handlers before starting the app
    register_signal_handlers()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
