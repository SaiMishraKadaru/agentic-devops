FROM python:3.10-slim
WORKDIR /app

COPY app/app.py .
CMD ["python", "app.py"]