FROM python:alpine3.22

WORKDIR /app

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 8080


#HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health || exit 1
HEALTHCHECK --interval=30s --timeout=3s CMD python healthcheck.py || exit 1

ENTRYPOINT ["uvicorn","app:app","--host","0.0.0.0","--port","8080"]


