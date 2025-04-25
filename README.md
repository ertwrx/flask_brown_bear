# 🐻 Flask Brown Bear

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Docker Image](https://img.shields.io/badge/Docker_Image-v3-blue.svg)](https://hub.docker.com/r/ertwrx/flask_brown_bear)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2.0-green.svg)](https://gunicorn.org/)
[![12 Factor App](https://img.shields.io/badge/12--Factor-Compliant-brightgreen.svg)](https://12factor.net/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Interactive](https://img.shields.io/badge/Interactive-Yes-success.svg)]()
[![Kids Friendly](https://img.shields.io/badge/Kids_Friendly-Yes-ff69b4.svg)]()



A Flask web application based on Eric Carle's classic children's book "Brown Bear, Brown Bear, What Do You See?". This interactive app was created as a dedication to my son, for whom this is a beloved favorite book.

![Flask Brown Bear](static/images/brown_bear.jpg)

## 📖 Description

Flask Brown Bear brings the magic of Eric Carle's timeless children's book to life in a digital format. The application features:

- 🖼️ Interactive images of the animals from the book
- 🔊 Animal sounds that play when images are clicked
- 📱 Fullscreen toggle functionality for better viewing experience
- 👶 Simple, child-friendly interface

Each animal from the story is represented with vibrant images and corresponding sounds, creating an engaging, multimedia experience that honors the spirit of the original book.

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/ertwrx/flask_brown_bear.git

# Navigate to the project directory
cd flask_brown_bear

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

## 🎮 Usage

### 🏃 Running the Application

Choose one of the following methods to run the application:

```bash
# Option 1: Flask development server ⚗️
flask run

# Option 2: Using Python entrypoint 🐍
python run.py

# Option 3: Using Gunicorn 🦄
gunicorn --bind 0.0.0.0:5000 'main:create_app()'
```

### 🐋 Running with Docker

**Using Docker directly:**

```bash
docker build -t flask_brown_bear .
docker run -p 5000:5000 -e FLASK_ENV=development flask_brown_bear
```

**🐙 Using Docker Compose:**

```bash
docker-compose up
```

### 🎯 Using the Application

1. Open your web browser and go to `http://localhost:5000`
2. Navigate through the animals using the navigation buttons
3. Click on any animal image to:
   - Toggle fullscreen view
   - Hear the animal's sound

## 🛠️ Administrative Tools

### 🧰 Using admin.py

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

### 🔑 Using generate_key.py

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

This application follows the 12-Factor App methodology:

1. **🧬 Codebase**: One codebase tracked in Git
2. **📦 Dependencies**: Explicitly declared in requirements.txt
3. **⚙️ Config**: Environment variable configuration
4. **🔌 Backing Services**: Treated as attached resources
5. **🔨 Build, Release, Run**: Strict separation of build and run stages
6. **💻 Processes**: Application runs as stateless processes
7. **🔒 Port Binding**: Self-contained with port binding
8. **⚡ Concurrency**: Scalable through process model
9. **🔄 Disposability**: Fast startup and graceful shutdown
10. **🔍 Dev/Prod Parity**: Keep development and production as similar as possible
11. **📊 Logs**: Treated as event streams
12. **🧩 Admin Processes**: Run admin tasks as one-off processes

## 📁 Project Structure

```
flask_brown_bear/
├── app.py                  # Main Flask application
├── run.py                  # Entry point for running the application
├── main.py                 # Application factory function
├── admin.py                # Administrative commands
├── generate_key.py         # Secret key generator
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Example environment variables
├── static/
│   ├── css/
│   │   └── style.css       # Application styling
│   ├── images/             # Animal images
│   │   └── ...
│   ├── js/
│   │   └── script.js       # JavaScript for interactivity
│   └── sounds/             # Animal sound files
│       └── ...
└── templates/
    └── index.html          # Main HTML template
```

## 💻 Technologies Used

- **🔙 Backend:** Flask (Python web framework)
- **🔝 Frontend:** HTML, CSS, JavaScript
- **🎵 Media:** JPG images and MP3 sound files
- **📦 Containerization:** Docker, Docker Compose
- **🚀 Deployment:** Gunicorn WSGI server

## 💡 Inspiration

This application is inspired by Eric Carle's "Brown Bear, Brown Bear, What Do You See?", a cherished children's book known for its rhythmic text and colorful animal illustrations. The book follows a sequence of animals, each seeing another animal, creating a memorable pattern that children love.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Note: While the code for this application is released under the MIT License, please be aware that "Brown Bear, Brown Bear, What Do You See?" is the intellectual property of Eric Carle and Bill Martin Jr. This application is intended for personal educational use and not for commercial purposes related to the book's content.

## 🙏 Acknowledgements

- Eric Carle and Bill Martin Jr. for creating the wonderful book that inspired this project
- Dedicated to my son, whose love for this book motivated the creation of this application
