FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=3s --retries=5 --start-period=5s CMD ["python", "healthcheck_http.py"]

CMD ["python", "app.py"]
