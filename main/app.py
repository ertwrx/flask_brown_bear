# main/app.py

from pathlib import Path
from . import create_app

# Flask expects `app` to be exposed at module level
app = create_app()

# This block only runs when executing this file directly (e.g. `python main/app.py`)
if __name__ == '__main__':
    # Optional: Debug DB info when running manually
    db_path = Path(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    print(f"Database file path: {db_path}")
    print(f"Database file exists: {db_path.exists()}")
    print(f"Database directory exists: {db_path.parent.exists()}")

    app.run(host='0.0.0.0', port=5000)

