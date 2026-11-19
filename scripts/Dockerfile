FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir prometheus-client==0.21.1
COPY log_to_metrics.py .
ENV PYTHONUNBUFFERED=1
USER 65534:65534
EXPOSE 8082
CMD ["python", "log_to_metrics.py"]
