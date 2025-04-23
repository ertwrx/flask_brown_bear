# This file is no longer the main entry point
# It can be used for direct application instantiation if needed

from flask import render_template
from . import create_app

# This is only for direct execution of this file
# Normally, the application should be created via the factory in __init__.py
app = create_app()

# No need to duplicate routes here - they should be in routes/__init__.py

if __name__ == '__main__':
    # This is only for development convenience when running this file directly
    # In production, the app will be served by gunicorn or similar
    app.run(host='0.0.0.0', port=5000)
