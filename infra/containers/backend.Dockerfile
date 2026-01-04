# Change from 3.13 to 3.11 to match Debian Bookworm's python3-uno
FROM docker.io/library/python:3.13-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-script-provider-python \
    python3-uno \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Setup user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Setup Python environment
COPY apps/backendworker/requirements.txt .

# 1. Create venv FIRST 
# 2. Use --system-site-packages so it can see /usr/lib/python3/dist-packages
RUN python3 -m venv venv --system-site-packages
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt 

# Copy application and the start script
COPY apps/backendworker/albayanworker ./albayanworker
COPY infra/containers/start_app.sh .
RUN chmod +x start_app.sh && chown -R appuser:appgroup /app

# Crucial environment variables
ENV HOME=/tmp
ENV PYTHONPATH="/usr/lib/python3/dist-packages"
ENV PYTHONUNBUFFERED=1

USER appuser
EXPOSE 8080

CMD ["./start_app.sh"]