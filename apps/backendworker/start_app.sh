#!/bin/bash
# Start LibreOffice listener in the background
soffice --headless --accept="socket,host=localhost,port=2002;urp;" --norestore --nolockcheck &

# Wait for soffice to be ready
sleep 2

# Start Python
exec ./venv/bin/uvicorn albayanworker.main:app --host 0.0.0.0 --port 8080