from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai
from app.config import settings

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

# Include routers
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])

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
