# Flask Brown Bear 🐻

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![12-Factor](https://img.shields.io/badge/12--factor-compliant-brightgreen.svg)](https://12factor.net/)

A simple, well-structured Flask application demonstrating a book API for Eric Carle's "Brown Bear, Brown Bear, What Do You See?" Complete with Docker support, multiple deployment options, and 12-factor methodology compliance.

## 📋 Features

- RESTful API for the "Brown Bear" book content
- Multiple deployment options (Flask dev server, Gunicorn, Docker)
- Structured as a proper Python package
- Configurable through environment variables
- Health check endpoint
- Clean modular architecture

## 🚀 Quick Start

### Running Locally

1. 🐏 Clone the repository:
   ```bash
   git clone https://github.com/ertwrx/flask_brown_bear.git
   cd flask_brown_bear
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application (choose one⚗️🐍🦄):
   ```bash
   # Option 1: Flask development server
   flask run
   
   # Option 2: Using Python entrypoint
   python run.py
   
   # Option 3: Using Gunicorn
   gunicorn --bind 0.0.0.0:5000 'main:create_app()'
   ```

### 🐋Running with Docker

#### Using Docker directly:
```bash
docker build -t flask_brown_bear .
docker run -p 5000:5000 flask_brown_bear
```

#### 🐙Using Docker Compose:
```bash
docker-compose up
```

## Administrative Tools

### Using admin.py

The `admin.py` script provides administrative commands for managing the application following the 12-factor app methodology. It lets you perform maintenance tasks using the same codebase and environment as the main application.

Available commands:

```bash
# Initialize the database tables
python admin.py db:init

# Seed the database with sample data (book pages and animals)
python admin.py db:seed

# Reset the database (WARNING: destroys all data)
python admin.py db:reset

# Backup the database to a timestamped file in the backups directory
python admin.py db:backup

# Restore the database from a previous backup
python admin.py db:restore

# Check and validate application configuration
python admin.py check:config

# Run application health checks
python admin.py health:check

# Clear application caches
python admin.py cache:clear
```

### Using generate_key.py

The `generate_key.py` script creates a secure random secret key for your Flask application.

```bash
# Generate a new secret key
python generate_key.py

# The script will output a secure random key that you can add to your .env file
# Example output:
# Generated SECRET_KEY: fT5cUq8lKJr0e3iYbHx2vPzN7wDmVgS9
# Add this to your .env file:
# SECRET_KEY=fT5cUq8lKJr0e3iYbHx2vPzN7wDmVgS9
```

After running the script, copy the generated key and add it to your `.env` file or environment variables.


## 🔄 12-Factor Compliance

This application follows the [12-Factor App](https://12factor.net/) methodology:

1. **Codebase**: One codebase tracked in Git
2. **Dependencies**: Explicitly declared in requirements.txt
3. **Config**: Environment variable configuration
4. **Backing Services**: Treated as attached resources
5. **Build, Release, Run**: Strict separation of build and run stages
6. **Processes**: Application runs as stateless processes
7. **Port Binding**: Self-contained with port binding
8. **Concurrency**: Scalable through process model
9. **Disposability**: Fast startup and graceful shutdown
10. **Dev/Prod Parity**: Keep development and production as similar as possible
11. **Logs**: Treated as event streams
12. **Admin Processes**: Run admin tasks as one-off processes

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
