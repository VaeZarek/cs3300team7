FROM python:latest
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chmod=755 ./job_connect .
