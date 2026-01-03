FROM python:3.13-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-script-provider-python \
    python3-uno \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Setup user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Setup Python environment
COPY requirements.txt .
RUN python3 -m venv venv --system-site-packages
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt 

# Copy application and the start script
COPY albayanworker ./albayanworker
COPY start.sh .
RUN chmod +x start.sh && chown -R appuser:appgroup /app

ENV HOME=/tmp
USER appuser

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Use the script to launch both processes
CMD ["./start.sh"]