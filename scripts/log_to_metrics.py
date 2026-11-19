"""Count synthetic HTTP logs. Metrics reset when this process restarts."""
import json
import os
import time
from prometheus_client import Counter, start_http_server

REQUESTS = Counter("http_requests_total", "Parsed HTTP requests", ["method", "status"])
STATUS = Counter("http_status_codes_total", "Parsed HTTP responses", ["status"])
BYTES = Counter("http_response_size_bytes_total", "Response bytes in parsed logs", ["method"])
INVALID = Counter("log_exporter_invalid_lines_total", "Invalid or incomplete log lines")
LOG_FILE = "/var/log/generated-logs.txt"
METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}

def parse_log_line(line):
    try:
        data = json.loads(line)
        method = str(data.get("method", "UNKNOWN")).upper()
        method = method if method in METHODS else "OTHER"
        status = str(data["status"])
        size = int(data.get("bytes", 0))
        if len(status) != 3 or not status.isdigit() or size < 0:
            raise ValueError("invalid status or size")
        REQUESTS.labels(method=method, status=status).inc()
        STATUS.labels(status=status).inc()
        BYTES.labels(method=method).inc(size)
    except (ValueError, TypeError, KeyError, AttributeError):
        INVALID.inc()

def follow(path):
    position = 0
    identity = None
    while True:
        try:
            stat = os.stat(path)
            current = (stat.st_dev, stat.st_ino)
            if current != identity or stat.st_size < position:
                position, identity = 0, current
            with open(path, encoding="utf-8") as stream:
                stream.seek(position)
                while True:
                    before = stream.tell()
                    line = stream.readline()
                    if not line or not line.endswith("\n"):
                        position = before
                        break
                    parse_log_line(line)
                    position = stream.tell()
        except (OSError, UnicodeError) as exc:
            print(f"Log read error: {exc}", flush=True)
        time.sleep(0.5)

if __name__ == "__main__":
    start_http_server(8082)
    follow(LOG_FILE)
