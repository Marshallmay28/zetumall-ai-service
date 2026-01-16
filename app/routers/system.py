from fastapi import APIRouter
from starlette.responses import PlainTextResponse
import time
import psutil
import os

router = APIRouter()

start_time = time.time()

@router.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """
    Simple Prometheus-style metrics
    """
    uptime = time.time() - start_time
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    # Prometheus format
    metrics_data = [
        f'# HELP app_uptime_seconds Uptime of the application in seconds',
        f'# TYPE app_uptime_seconds gauge',
        f'app_uptime_seconds {uptime}',
        
        f'# HELP app_memory_usage_bytes Memory usage in bytes',
        f'# TYPE app_memory_usage_bytes gauge',
        f'app_memory_usage_bytes {memory_info.rss}',
        
        f'# HELP app_cpu_percent CPU usage percent',
        f'# TYPE app_cpu_percent gauge',
        f'app_cpu_percent {process.cpu_percent()}',
    ]
    
    return "\n".join(metrics_data)
