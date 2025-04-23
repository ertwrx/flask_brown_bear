# ---- Build Stage ----
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system deps for compiling packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps into a venv
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# ---- Final Stage ----
FROM python:3.12-slim

# Set environment and copy virtual environment from builder
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy the virtual environment and app code
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Expose app port
EXPOSE 5000

# Start the app using Gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "main.app:app"]
