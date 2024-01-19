# gunicorn.conf.py

bind = "0.0.0.0:5000"  # Set the host and port for Gunicorn
workers = 4            # Number of worker processes
threads = 2            # Number of worker threads per process
worker_class = "gthread"  # Worker processes class
timeout = 120           # Request timeout in seconds
preload_app = True      # Preload the application before forking worker processes
