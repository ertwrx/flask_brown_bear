#!/usr/bin/env python
"""
admin.py - Administrative tasks for Flask Brown Bear application

This script provides one-off administrative commands that follow the 12-factor
app methodology. It uses the same codebase and environment as the main application.

Usage:
    python admin.py <command> [options]

Commands:
    db:init        - Initialize the database tables
    db:seed        - Seed the database with sample data (including static files)
    db:reset       - Reset the database (WARNING: destroys all data)
    db:backup      - Backup the database to a file
    db:restore     - Restore the database from a backup
    check:config   - Check and validate configuration
    health:check   - Run application health checks
    cache:clear    - Clear application caches
"""

import os
import sys
import argparse
import shutil
import json
import datetime
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
# In the health_check function
from sqlalchemy import text, inspect

# Load environment variables first
load_dotenv()

# Set up path to allow importing from the application
script_path = Path(__file__).resolve()
project_root = script_path.parent
sys.path.insert(0, str(project_root))

# Import application components after setting up the path
from main import create_app, db
from main.models import Page, Book, Animal, StaticFile
from main.config import get_config


def db_init():
    """Initialize database tables."""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully")


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


def upload_static_files(app_context):
    """Upload all static files to the database."""
    # The base directory for static files
    static_dir = Path(app_context.root_path) / 'static'

    if not static_dir.exists():
        print(f"❌ Static directory {static_dir} does not exist!")
        return False

    print(f"Uploading files from {static_dir}")

    # Count files for progress reporting
    total_files = sum(1 for _ in static_dir.glob('**/*') if _.is_file())
    if total_files == 0:
        print("No static files found to upload")
        return True
    
    processed = 0
    success_count = 0

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
                    success_count += 1
                    print(f"Added file: {rel_path}")
                except Exception as e:
                    print(f"❌ Error uploading {rel_path}: {e}")

            processed += 1
            if processed % 10 == 0 or processed == total_files:
                print(f"Progress: {processed}/{total_files} files processed")

    # Commit all changes
    db.session.commit()
    print(f"✅ {success_count}/{total_files} static files uploaded to database!")
    return True


def db_seed():
    """Seed the database with initial data and static files."""
    app = create_app()
    with app.app_context():
        # Check if book data already exists
        if Book.query.count() > 0:
            print("⚠️ Database already contains book data.")
        else:
            # Create the book
            book = Book(title="Brown Bear, Brown Bear, What Do You See?", author="Eric Carle")
            db.session.add(book)

            # Create animals and pages
            animals = [
                "Brown Bear", "Red Bird", "Yellow Duck", "Blue Horse",
                "Green Frog", "Purple Cat", "White Dog", "Black Sheep",
                "Goldfish", "Teacher", "Children"
            ]

            for i, animal_name in enumerate(animals, 1):
                animal = Animal(name=animal_name)
                db.session.add(animal)

                # Create the corresponding page
                page = Page(
                    number=i,
                    content=f"{animal_name}, {animal_name}, what do you see?",
                    book_id=1,
                    animal_id=i
                )
                db.session.add(page)

            db.session.commit()
            print(f"✅ Database seeded with book and {len(animals)} animals/pages")
        
        # Check if static files exist in the database
        static_files_count = StaticFile.query.count()
        if static_files_count > 0:
            print(f"⚠️ Database already contains {static_files_count} static files.")
            proceed = input("Do you want to upload additional static files? (yes/no): ")
            if proceed.lower() != "yes":
                return
        
        # Upload static files
        upload_static_files(app)


def db_reset():
    """Reset the database (drop and recreate tables)."""
    confirm = input("⚠️ WARNING: This will delete all data. Type 'yes' to confirm: ")
    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database reset complete")


def db_backup():
    """Backup SQLite database to a timestamped file."""
    config = get_config()
    db_path = config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')

    # Create backups directory if it doesn't exist
    backup_dir = project_root / 'backups'
    backup_dir.mkdir(exist_ok=True)

    # Create timestamped backup file
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"app_db_backup_{timestamp}.db"

    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to {backup_path}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")


def db_restore():
    """Restore database from a backup file."""
    backup_dir = project_root / 'backups'
    if not backup_dir.exists():
        print("❌ No backups directory found")
        return

    # List available backups
    backups = list(backup_dir.glob('*.db'))
    if not backups:
        print("❌ No backup files found in backups directory")
        return

    print("Available backups:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup.name}")

    # Ask user to select a backup
    try:
        selection = int(input("Enter the number of the backup to restore: "))
        selected_backup = backups[selection - 1]
    except (ValueError, IndexError):
        print("❌ Invalid selection")
        return

    # Get database path
    config = get_config()
    db_path = config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')

    # Confirm before overwriting
    confirm = input(f"⚠️ This will overwrite the current database with {selected_backup.name}. Type 'yes' to confirm: ")
    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return

    try:
        # Stop the app if it's running
        # In a production environment, you might need more sophisticated handling here

        # Copy the backup over the current database
        shutil.copy2(selected_backup, db_path)
        print(f"✅ Database restored from {selected_backup.name}")
    except Exception as e:
        print(f"❌ Restore failed: {e}")


def check_config():
    """Check and validate configuration."""
    app = create_app()
    config_dict = {key: value for key, value in app.config.items()
                  if not key.startswith('_') and key.isupper()}

    # Check critical configuration elements
    critical_keys = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
    issues = []

    for key in critical_keys:
        if key not in config_dict:
            issues.append(f"Missing critical config: {key}")
        elif not config_dict[key]:
            issues.append(f"Empty critical config: {key}")

    # Check security of SECRET_KEY
    if config_dict.get('SECRET_KEY') == 'dev-key-please-change-in-production':
        issues.append("WARNING: Using default development SECRET_KEY")

    # Check database configuration
    db_uri = config_dict.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri.startswith('sqlite') and app.config.get('ENV') == 'production':
        issues.append("WARNING: Using SQLite in production is not recommended")

    # Print configuration (excluding sensitive values)
    print("Application Configuration:")
    for key, value in config_dict.items():
        if key in ['SECRET_KEY']:
            value = '*****' if value else 'NOT SET'
        print(f"  {key}: {value}")

    # Print issues
    if issues:
        print("\nConfiguration Issues:")
        for issue in issues:
            print(f"  ⚠️ {issue}")
    else:
        print("\n✅ No configuration issues detected")


def health_check():
    """Run health checks on the application."""
    app = create_app()
    checks = {
        "database": False,
        "filesystem": False,
        "config": False
    }

    # Check database connection
    try:
     with app.app_context():
        with db.engine.connect() as connection:
            connection.execute(db.text("SELECT 1"))
        checks["database"] = True
    except Exception as e:
     print(f"❌ Database check failed: {e}")

    # Check filesystem access
    try:
        test_path = project_root / 'test_write.tmp'
        with open(test_path, 'w') as f:
            f.write('test')
        test_path.unlink()
        checks["filesystem"] = True
    except Exception as e:
        print(f"❌ Filesystem check failed: {e}")

    # Check configuration
    try:
        app.config['TEST_HEALTH_CHECK'] = True
        checks["config"] = app.config['TEST_HEALTH_CHECK'] is True
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")

    # Print results
    print("Health Check Results:")
    all_passed = True
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        if not result:
            all_passed = False
        print(f"  {check_name}: {status}")

    return 0 if all_passed else 1


def cache_clear():
    """Clear application caches."""
    cache_paths = [
        project_root / '__pycache__',
        project_root / 'main' / '__pycache__',
        project_root / 'main' / 'routes' / '__pycache__',
        project_root / 'main' / 'models' / '__pycache__',
    ]

    # Find and remove cache files
    for path in cache_paths:
        if path.exists():
            shutil.rmtree(path)
            print(f"Cleared: {path}")

    # Remove .pyc files
    pyc_files = list(project_root.glob('**/*.pyc'))
    for file in pyc_files:
        file.unlink()
        print(f"Removed: {file}")

    print("✅ Cache cleared")


def main():
    parser = argparse.ArgumentParser(description='Flask Brown Bear Admin Commands')
    parser.add_argument('command', help='Command to execute')

    args = parser.parse_args()
    command = args.command

    # Command mapping
    commands = {
        'db:init': db_init,
        'db:seed': db_seed,
        'db:reset': db_reset,
        'db:backup': db_backup,
        'db:restore': db_restore,
        'check:config': check_config,
        'health:check': health_check,
        'cache:clear': cache_clear,
    }

    if command in commands:
        return commands[command]()
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        for cmd in commands.keys():
            print(f"  - {cmd}")
        return 1


if __name__ == '__main__':
 sys.exit(main())
