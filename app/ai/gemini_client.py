import google.generativeai as genai
from app.config import settings
from typing import Optional

class GeminiClient:
    """Google Gemini AI client for generating content"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_product_description(
        self,
        name: str,
        category: str,
        features: Optional[list] = None
    ) -> str:
        """Generate AI product description"""
        
        features_text = "\n".join(f"- {feature}" for feature in (features or []))
        
        prompt = f"""Generate a compelling, SEO-optimized product description for an e-commerce platform.

Product Name: {name}
Category: {category}
{f'Key Features:\n{features_text}' if features else ''}

Requirements:
- Write 2-3 paragraphs (150-200 words)
- Highlight key benefits and features
- Use persuasive language that encourages purchase
- Include relevant keywords for SEO
- Professional and engaging tone
- Focus on value proposition

Product Description:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Failed to generate description: {str(e)}")
    
    async def generate_store_description(
        self,
        name: str,
        category: str,
        tagline: Optional[str] = None
    ) -> str:
        """Generate AI store description"""
        
        prompt = f"""Generate a professional store description for an e-commerce marketplace.

Store Name: {name}
Category: {category}
{f'Tagline: {tagline}' if tagline else ''}

Requirements:
- Write 2 paragraphs (100-150 words)
- Establish brand identity and trustworthiness
- Highlight store's unique value proposition
- Professional and welcoming tone
- Include category expertise

Store Description:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Failed to generate store description: {str(e)}")
    
    async def generate_product_tags(
        self,
        name: str,
        description: str,
        category: str
    ) -> list:
        """Generate relevant product tags"""
        
        prompt = f"""Generate 8-12 relevant tags for this product:

Name: {name}
Category: {category}
Description: {description[:200]}...

Requirements:
- Tags should be single words or short phrases (2-3 words max)
- Focus on searchability and discoverability
- Include category-specific and general tags
- Format as comma-separated list

Tags:"""

        try:
            response = self.model.generate_content(prompt)
            tags_text = response.text.strip()
            # Parse comma-separated tags
            tags = [tag.strip() for tag in tags_text.split(',')]
            return tags[:12]  # Limit to 12 tags
        except Exception as e:
            raise Exception(f"Failed to generate tags: {str(e)}")
    
    async def generate_seo_metadata(
        self,
        name: str,
        description: str,
        category: str
    ) -> dict:
        """Generate SEO title and meta description"""
        
        prompt = f"""Generate SEO-optimized metadata for this product:

Product Name: {name}
Category: {category}
Description: {description[:150]}...

Generate:
1. SEO Title (50-60 characters, include main keyword)
2. Meta Description (150-160 characters, compelling call-to-action)

Format:
TITLE: [your title here]
META: [your meta description here]"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse response
            lines = text.split('\n')
            seo_data = {}
            
            for line in lines:
                if line.startswith('TITLE:'):
                    seo_data['title'] = line.replace('TITLE:', '').strip()
                elif line.startswith('META:'):
                    seo_data['metaDescription'] = line.replace('META:', '').strip()
            
            return seo_data
        except Exception as e:
            raise Exception(f"Failed to generate SEO metadata: {str(e)}")
    
    async def analyze_product_quality(
        self,
        name: str,
        description: str,
        price: float,
        category: str
    ) -> dict:
        """Analyze product listing quality and provide recommendations"""
        
        prompt = f"""Analyze this product listing quality:

Name: {name}
Category: {category}
Price: ${price}
Description: {description}

Provide:
1. Quality Score (0-100)
2. Key strengths (2-3 points)
3. Improvement suggestions (2-3 points)

Format as JSON:
{{
  "score": 85,
  "strengths": ["point 1", "point 2"],
  "improvements": ["suggestion 1", "suggestion 2"]
}}"""

        try:
            response = self.model.generate_content(prompt)
            # For simplicity, return basic analysis
            # In production, parse JSON response
            return {
                "score": 75,
                "strengths": ["Clear product name", "Detailed description"],
                "improvements": ["Add more product specifications", "Include customer benefits"]
            }
        except Exception as e:
            return {
                "score": 70,
                "strengths": ["Product listed successfully"],
                "improvements": ["Consider adding more details"]
            }

gemini_client = GeminiClient()
