from prometheus_client import start_http_server, Counter, Histogram
import time

# Define Prometheus metrics
log_ingested_counter = Counter('log_ingested_total', 'Total number of logs ingested')
audit_logged_counter = Counter('audit_logged_total', 'Total number of audit entries appended')
processing_time_histogram = Histogram('log_processing_seconds', 'Time taken to process each log')


def observe_log_ingestion():
    log_ingested_counter.inc()


def observe_audit_append():
    audit_logged_counter.inc()


def observe_processing_time(duration):
    processing_time_histogram.observe(duration)


def start_monitoring_server(port=9100):
    print(f"Starting Prometheus metrics server on port {port}...")
    start_http_server(port)



