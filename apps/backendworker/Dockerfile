FROM python:3.13-slim-bookworm



# Set the working directory for the application
WORKDIR /app
RUN apt install libreoffice libreoffice-script-provider-python python3-uno
RUN addgroup --system appgroup && adduser --system --ingroup unoapi unoapi
USER appuser

COPY requirements.txt .
#python3 -m venv venv --system-site-packages
RUN pip install -r requirements.txt 

COPY src ./src

ENV PYTHONUNBUFFERED 1
ENV PORT 8000
EXPOSE ${PORT}

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]