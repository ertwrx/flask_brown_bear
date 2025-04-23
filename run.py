import os
from main import create_app, register_signal_handlers

app = create_app()

if __name__ == '__main__':
    # Register signal handlers before starting the app
    register_signal_handlers()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    app.run(host=host, port=port)
