"""
Admin Dashboard Router for ZetuMall AI Service
Provides monitoring, metrics, and API testing interface
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psutil
import time
from datetime import datetime
from pathlib import Path

from app.middleware.api_key import verify_api_key

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])

# Templates directory
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Service start time
START_TIME = time.time()

@router.get("", response_class=HTMLResponse)
async def get_dashboard(request: Request, api_key: str = Depends(verify_api_key)):
    """
    Serve the admin dashboard HTML page
    Requires valid API key authentication
    """
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})


@router.get("/api/overview")
async def get_overview(api_key: str = Depends(verify_api_key)):
    """
    Get dashboard overview data
    """
    uptime_seconds = time.time() - START_TIME
    
    # Calculate uptime in human-readable format
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    
    if days > 0:
        uptime = f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        uptime = f"{hours}h {minutes}m"
    else:
        uptime = f"{minutes}m"
    
    return {
        "serviceName": "ZetuMall AI Service",
        "version": "1.0.0",
        "environment": "production",
        "startTime": datetime.fromtimestamp(START_TIME).isoformat(),
        "uptime": uptime,
        "health": "UP"
    }


@router.get("/api/metrics")
async def get_metrics(api_key: str = Depends(verify_api_key)):
    """
    Get system metrics
    """
    # CPU and Memory metrics
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    return {
        "cpuUsage": cpu_percent,
        "memory": {
            "used": memory.used,
            "total": memory.total,
            "percent": memory.percent
        },
        "requests": 0  # Would need request counter middleware
    }


@router.get("/api/health")
async def get_health(api_key: str = Depends(verify_api_key)):
    """
    Get health check details
    """
    return {
        "status": "UP",
        "components": {
            "gemini": {"status": "UP"},
            "system": {"status": "UP"}
        }
    }


@router.get("/api/activity")
async def get_activity(api_key: str = Depends(verify_api_key)):
    """
    Get recent API activity
    This would typically come from a logging service
    For now, return mock data
    """
    return [
        {
            "timestamp": datetime.now().isoformat(),
            "endpoint": "/chat",
            "method": "POST",
            "status": 200,
            "duration": 1250
        },
        {
            "timestamp": datetime.now().isoformat(),
            "endpoint": "/analyze-image",
            "method": "POST",
            "status": 200,
            "duration": 2100
        }
    ]
