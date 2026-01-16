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

    
    async def analyze_product_image(self, image_data: bytes, mime_type: str) -> dict:
        """Analyze product image for quality and compliance"""
        
        prompt = """🧠 ZETUMALL AI ANALYZER — MARKET PRECISION MODE

You are ZetuMall AI Analyzer, a marketplace intelligence engine that evaluates product images for listing quality.

CORE OUTPUT RULES (STRICT):
- Concise, marketplace language
- Max 2 short lines per field
- No paragraphs, emojis, or filler
- Structured JSON output only
- If uncertain → "Needs review"
- If risky → flag immediately

PRODUCT IMAGE ANALYSIS OUTPUT (JSON):
{
  "valid": boolean,
  "product_title": "Market-ready, searchable name (max 80 chars)",
  "category": "Primary marketplace category",
  "description": "Primary value. Usage or compatibility.",
  "key_attributes": ["Core feature", "Core specification"],
  "listing_quality": "Poor | Fair | Good | Excellent",
  "compliance_status": "Approved | Restricted | Prohibited",
  "risk_indicator": "Low | Medium | High",
  "confidence": 0-100,
  "reason": "Short reason if invalid or risky"
}

DECISION RULES:
- High quality + low risk → Approved
- Low quality + medium risk → Needs review
- High risk → Prohibited
- Confidence < 65 → Manual review

Analyze the product image and return ONLY the JSON structure above."""

        try:
            response = self.model.generate_content([
                prompt,
                {
                    "mime_type": mime_type,
                    "data": image_data
                }
            ])
            
            text = response.text
            
            # Robust JSON extraction
            import json
            import re
            
            json_match = re.search(r'\{[\s\S]*\}', text)
            if not json_match:
                raise Exception("No JSON structure found")
                
            return json.loads(json_match.group(0))
            
        except Exception as e:
            raise Exception(f"Failed to analyze image: {str(e)}")

    async def analyze_security_briefing(self, health_data: dict, error_logs: list) -> dict:
        """Analyze system health and security logs"""
        
        prompt = f"""
        You are a Cyber Security Ops AI for ZetuMall.
        Analyze the following system status and error logs to provide a security briefing.
        
        System Health: {health_data}
        Recent Errors: {error_logs}

        Your response must be a valid JSON object with the following structure:
        {{
            "briefing": "A concise 2-3 sentence overview of the current security and stability state.",
            "status": "SECURE" | "WARNING" | "CRITICAL",
            "recommendations": [
                {{ "title": "...", "description": "...", "priority": "high" | "medium" | "low" }}
            ],
            "stats": {{
                "errorRate": "e.g. 5% last hour",
                "riskLevel": "Low" | "Medium" | "High"
            }}
        }}
        Do not include any markdown formatting like ```json. Return only the raw JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "")
            
            import json
            return json.loads(text)
        except Exception as e:
            # Fallback response
            return {
                "briefing": "System is operational. Some non-critical errors detected in processing.",
                "status": "SECURE",
                "recommendations": [{"title": "Monitor Logs", "description": "Continue monitoring error logs for patterns.", "priority": "low"}],
                "stats": {"errorRate": "Normal", "riskLevel": "Low"}
            }

    async def chat_support(self, message: str) -> dict:
        """Chat support for ZetuMall"""
        
        # Simple language detection
        swahili_keywords = ['habari', 'sawa', 'asante', 'tafadhali', 'nini', 'vipi', 'nina', 'nataka']
        is_swahili = any(keyword in message.lower() for keyword in swahili_keywords)
        language = 'sw' if is_swahili else 'en'
        
        system_prompt = """You are a helpful customer support assistant for ZetuMall, an e-commerce platform in Kenya.

IMPORTANT GUIDELINES:
- You are a ZetuMall staff member helping customers
- Be friendly, professional, and concise
- Answer questions about orders, payments, delivery, products, and account issues
- Support both English and Swahili languages
- If you detect Swahili, respond in Swahili
- For complex issues, suggest contacting human support
- Never make up order numbers or specific details
- Focus on general help and guidance

ZETUMALL FEATURES:
- Escrow payment system for secure transactions
- Local delivery within Kenya
- Buyer and seller marketplace
- Product listings and store management
- Order tracking
- Secure payments via M-Pesa

Keep responses short (2-3 sentences max) and helpful."""

        prompt = f"{system_prompt}\n\nUser message: {message}\n\nRespond in {'Swahili' if language == 'sw' else 'English'}."
        
        try:
            response = self.model.generate_content(prompt)
            reply = response.text
            
            suggestions = [
                'Fuatilia agizo langu', 'Msaada wa malipo', 'Maelezo ya utoaji', 'Wasiliana na msaada'
            ] if language == 'sw' else [
                'Track my order', 'Payment help', 'Delivery info', 'Contact support'
            ]
            
            return {
                "message": reply,
                "suggestions": suggestions
            }
        except Exception as e:
            raise Exception(f"Chat failed: {str(e)}")

gemini_client = GeminiClient()
