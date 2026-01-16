from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai, system, admin_dashboard
from app.config import settings
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.auth_middleware import ApiKeyMiddleware

app = FastAPI(
    title="ZetuMall AI Service",
    version="1.0.0",
    description="AI-powered features for ZetuMall using Google Gemini"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Authentication middleware
app.add_middleware(ApiKeyMiddleware)

# Include routers
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(system.router, tags=["System"])
app.include_router(admin_dashboard.router)  # Admin Dashboard

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "zetumall-ai-service",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ZetuMall AI Service",
        "docs": "/docs",
        "health": "/health"
    }
