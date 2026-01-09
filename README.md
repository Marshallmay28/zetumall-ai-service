# ZetuMall AI Service

AI-powered microservice for ZetuMall e-commerce platform using Google Gemini API and FastAPI.

## 🎯 Features

- **Product Description Generation** - AI-generated compelling product descriptions
- **Store Description Generation** - Professional store descriptions
- **Product Tags** - Auto-generate relevant search tags
- **SEO Optimization** - Generate SEO titles and meta descriptions
- **Quality Analysis** - Analyze and score product listings

## 🏗️ Architecture

- **Framework**: FastAPI
- **AI Engine**: Google Gemini Pro
- **Authentication**: Supabase JWT
- **Database**: Supabase PostgreSQL (shared with Spring Boot)

## 📁 Project Structure

```
zetumall-ai-service/
├── main.py                      # FastAPI application
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── app/
│   ├── config.py               # Configuration settings
│   ├── auth/
│   │   └── supabase_auth.py    # JWT authentication
│   ├── ai/
│   │   └── gemini_client.py    # Gemini AI client
│   └── routers/
│       └── ai.py               # AI API endpoints
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key
- Supabase account

### Installation

1. **Create virtual environment**:
   ```bash
   cd zetumall-ai-service
   python -m venv venv
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   copy .env.example .env
   ```
   
   Fill in your credentials in `.env`:
   ```env
   GEMINI_API_KEY=your-gemini-api-key
   SUPABASE_URL=your-supabase-url
   SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_JWT_SECRET=your-jwt-secret
   ```

5. **Run the service**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

### Generate Product Description
```bash
POST /api/ai/description
Authorization: Bearer <jwt_token>

{
  "name": "iPhone 15 Pro",
  "category": "Electronics",
  "features": ["A17 Pro chip", "Titanium design", "48MP camera"]
}
```

### Generate Store Description
```bash
POST /api/ai/generate-store-description
Authorization: Bearer <jwt_token>

{
  "name": "Tech Haven",
  "category": "Electronics",
  "tagline": "Your Premium Tech Destination"
}
```

### Generate Product Tags
```bash
POST /api/ai/tags
Authorization: Bearer <jwt_token>

{
  "name": "MacBook Pro 16",
  "description": "Powerful laptop for professionals",
  "category": "Computers"
}
```

### Generate SEO Metadata
```bash
POST /api/ai/seo
Authorization: Bearer <jwt_token>

{
  "name": "Wireless Headphones",
  "description": "Premium noise-cancelling headphones",
  "category": "Audio"
}
```

### Analyze Product Quality
```bash
POST /api/ai/quality-analysis
Authorization: Bearer <jwt_token>

{
  "name": "Product Name",
  "description": "Product description...",
  "price": 99.99,
  "category": "Category"
}
```

## 🔐 Authentication

All endpoints require Supabase JWT authentication in the `Authorization` header:

```
Authorization: Bearer <your_supabase_jwt_token>
```

## 🌐 CORS Configuration

Configured to allow requests from:
- `http://localhost:3000` (Next.js frontend)
- `http://localhost:8080` (Spring Boot backend)

## 📊 Interactive Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

### Using cURL

```bash
# Get health status
curl http://localhost:8000/health

# Generate product description
curl -X POST http://localhost:8000/api/ai/description \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smart Watch",
    "category": "Wearables",
    "features": ["Heart rate monitor", "GPS tracking"]
  }'
```

### Using Python

```python
import httpx

async def test_ai_service():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/ai/description",
            headers={"Authorization": "Bearer YOUR_JWT_TOKEN"},
            json={
                "name": "Smart Watch",
                "category": "Wearables"
            }
        )
        print(response.json())
```

## 🔗 Integration with Spring Boot

The Spring Boot backend can call this service:

```java
@Service
public class AiServiceClient {
    private final String AI_SERVICE_URL = "http://localhost:8000";
    
    public String generateDescription(String name, String category) {
        // Make HTTP request to AI service
        // Return generated description
    }
}
```

## 🚢 Deployment

### Railway

1. Create new project on Railway
2. Connect GitHub repository
3. Add environment variables
4. Deploy automatically

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t zetumall-ai-service .
docker run -p 8000:8000 --env-file .env zetumall-ai-service
```

## 📝 Development

```bash
# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Format code
black app/

# Type checking
mypy app/
```

## 🔧 Configuration

All configuration is managed via environment variables in `.env`:

- `DATABASE_URL` - PostgreSQL connection string
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key
- `SUPABASE_JWT_SECRET` - JWT secret for token validation
- `GEMINI_API_KEY` - Google Gemini API key
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)
- `PORT` - Server port (default: 8000)

## 📄 License

MIT License

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request
