import os
import mimetypes
from pathlib import Path
from flask import Flask
from main import create_app, db
from sqlalchemy import inspect

# First ensure models are properly imported and the static_files table exists
app = create_app()

with app.app_context():
    # Import here to ensure it's available
    from main.models import StaticFile
    
    # Create all tables if they don't exist
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Database tables before: {tables}")
    
    if 'static_files' not in tables:
        print("Creating static_files table...")
        db.create_all()
        tables = inspector.get_table_names()
        print(f"Database tables after: {tables}")

    # Now upload files
    def get_content_type(file_path):
        """Determine the content type of a file."""
        guessed_type = mimetypes.guess_type(file_path)[0]
        if guessed_type:
            return guessed_type
        
        # Default content types for common extensions
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.js': 'application/javascript',
            '.css': 'text/css',
            '.html': 'text/html',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.mp3': 'audio/mpeg',
            '.mp4': 'video/mp4',
            '.ico': 'image/x-icon',
        }
        return content_types.get(ext, 'application/octet-stream')

    def upload_static_files():
        """Upload all static files to the database."""
        # The base directory for static files
        static_dir = Path(app.root_path) / 'static'
        
        if not static_dir.exists():
            print(f"Static directory {static_dir} does not exist!")
            return
        
        print(f"Uploading files from {static_dir}")
        
        # Count files for progress reporting
        total_files = sum(1 for _ in static_dir.glob('**/*') if _.is_file())
        processed = 0
        
        # Walk through all files in the static directory
        for root, _, files in os.walk(static_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Create relative path from static directory
                rel_path = os.path.relpath(file_path, static_dir)
                
                # Check if file already exists in database
                existing = StaticFile.query.filter_by(filename=rel_path).first()
                
                if existing:
                    print(f"File {rel_path} already exists in database, skipping...")
                else:
                    try:
                        # Read file content
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        # Create database record
                        static_file = StaticFile(
                            filename=rel_path,
                            content_type=get_content_type(file_path),
                            data=file_data
                        )
                        
                        db.session.add(static_file)
                        print(f"Added file: {rel_path}")
                    except Exception as e:
                        print(f"Error uploading {rel_path}: {e}")
                
                processed += 1
                print(f"Progress: {processed}/{total_files} files processed")
        
        # Commit all changes
        db.session.commit()
        print("All static files uploaded to database!")

    upload_static_files()
