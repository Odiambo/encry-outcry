import time
from prometh_exp import (
    start_monitoring_server,
    observe_log_ingestion,
    observe_audit_append,
    observe_processing_time,
)

if __name__ == "__main__":
    start_monitoring_server()
    while True:
        observe_log_ingestion()
        observe_audit_append()
        observe_processing_time(0.25)
        time.sleep(5)
