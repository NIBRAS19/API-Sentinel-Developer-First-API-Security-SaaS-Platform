from celery import shared_task
from .engine import run_scan
@shared_task(bind=True)
def execute_scan(self,scan_id): return run_scan(scan_id)
