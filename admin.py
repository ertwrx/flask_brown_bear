#!/usr/bin/env python
"""
Admin processes for the Flask Brown Bear application.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import app
from main import create_app, db

def init_db():
    """Initialize the database with sample data."""
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if there are already entries
        from main.models import Page  # Import your model
        if Page.query.count() == 0:
            print("No pages found. Creating sample data...")
            # Add sample data
            # Example: db.session.add(Page(...))
            # db.session.commit()
            print("Sample data created.")
        else:
            print(f"Database already contains {Page.query.count()} pages.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python admin.py [command]")
        print("Commands:")
        print("  init_db - Initialize the database")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "init_db":
        init_db()
    else:
        print(f"Unknown command: {command}")
