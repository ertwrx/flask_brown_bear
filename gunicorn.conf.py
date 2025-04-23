import os
import multiprocessing

# Worker configuration
# Use the WEB_CONCURRENCY env var if defined, otherwise calculate based on CPU count
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
workers_per_core = float(workers_per_core_str)

if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
else:
    cores = multiprocessing.cpu_count()
    default_web_concurrency = workers_per_core * cores * 2
    web_concurrency = max(int(default_web_concurrency), 2)

# Host and port
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '5000')}"

# Worker configuration
workers = web_concurrency
worker_class = "gthread"
threads = int(os.getenv("THREADS_PER_WORKER", "4"))

# Timeouts
timeout = int(os.getenv("TIMEOUT", "120"))
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "120"))
keepalive = int(os.getenv("KEEP_ALIVE", "5"))

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.getenv("LOG_LEVEL", "info")

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Reload in development
