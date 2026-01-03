FROM python:3.13-slim-bookworm

# Set the working directory for the application
WORKDIR /app
RUN apt install libreoffice libreoffice-script-provider-python python3-uno
RUN addgroup --system appgroup && adduser --system --ingroup unoapi unoapi
USER appuser

COPY requirements.txt .
RUN python3 -m venv venv --system-site-packages
RUN ./venv/bin/pip install -r requirements.txt 

COPY albayanworker ./albayanworker

ENV PYTHONUNBUFFERED 1
ENV PORT 8080
EXPOSE ${PORT}

CMD ["./venv/bin/uvicorn", "albayanworker.main:app", "--host", "0.0.0.0", "--port", "8080"]