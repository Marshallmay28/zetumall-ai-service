from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
from app.auth.supabase_auth import get_current_user
from app.ai.gemini_client import gemini_client

router = APIRouter()

class ProductDescriptionRequest(BaseModel):
    name: str
    category: str
    features: Optional[List[str]] = None

class StoreDescriptionRequest(BaseModel):
    name: str
    category: str
    tagline: Optional[str] = None

class ProductTagsRequest(BaseModel):
    name: str
    description: str
    category: str

class SEORequest(BaseModel):
    name: str
    description: str
    category: str

class QualityAnalysisRequest(BaseModel):
    name: str
    description: str
    price: float
    category: str

class SecurityAnalysisRequest(BaseModel):
    health_data: dict
    error_logs: List[dict]

@router.post("/description")
async def generate_product_description(
    data: ProductDescriptionRequest,
    user: dict = Depends(get_current_user)
):
    """Generate AI-powered product description"""
    try:
        description = await gemini_client.generate_product_description(
            name=data.name,
            category=data.category,
            features=data.features
        )
        
        return {
            "success": True,
            "description": description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-store-description")
async def generate_store_description(
    data: StoreDescriptionRequest,
    user: dict = Depends(get_current_user)
):
    """Generate AI-powered store description"""
    try:
        description = await gemini_client.generate_store_description(
            name=data.name,
            category=data.category,
            tagline=data.tagline
        )
        
        return {
            "success": True,
            "description": description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tags")
async def generate_product_tags(
    data: ProductTagsRequest,
    user: dict = Depends(get_current_user)
):
    """Generate relevant product tags"""
    try:
        tags = await gemini_client.generate_product_tags(
            name=data.name,
            description=data.description,
            category=data.category
        )
        
        return {
            "success": True,
            "tags": tags
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seo")
async def generate_seo_metadata(
    data: SEORequest,
    user: dict = Depends(get_current_user)
):
    """Generate SEO-optimized metadata"""
    try:
        seo_data = await gemini_client.generate_seo_metadata(
            name=data.name,
            description=data.description,
            category=data.category
        )
        
        return {
            "success": True,
            "seo": seo_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quality-analysis")
async def analyze_product_quality(
    data: QualityAnalysisRequest,
    user: dict = Depends(get_current_user)
):
    """Analyze product listing quality"""
    try:
        analysis = await gemini_client.analyze_product_quality(
            name=data.name,
            description=data.description,
            price=data.price,
            category=data.category
        )
        
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-image")
async def analyze_product_image(
    image: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    """Analyze product image"""
    try:
        content = await image.read()
        analysis = await gemini_client.analyze_product_image(
            image_data=content,
            mime_type=image.content_type
        )
        
        return {
            "success": True,
            **analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/security-analysis")
async def analyze_security(
    data: SecurityAnalysisRequest,
    user: dict = Depends(get_current_user)
):
    """Generate security briefing"""
    try:
        analysis = await gemini_client.analyze_security_briefing(
            health_data=data.health_data,
            error_logs=data.error_logs
        )
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
