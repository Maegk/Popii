# Quick Start Guide

Get started with the Creative Fatigue Detection System in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14+ (or use Docker)
- Redis 7+ (or use Docker)
- API keys (at least one):
  - Meta Ads API token (optional, for full integration)
  - Anthropic API key OR OpenAI API key (for creative generation)

## Option 1: Docker Setup (Recommended)

The easiest way to get started:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Popii

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env and add your API keys
nano .env  # or use your preferred editor

# Required: Add at least one AI API key
ANTHROPIC_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here

# Optional: Meta Ads API (for production use)
META_ACCESS_TOKEN=your_token
META_AD_ACCOUNT_ID=act_123456789

# 4. Start all services with Docker
docker-compose up -d

# 5. Check that everything is running
curl http://localhost:8000/health
```

That's it! The system is now running at `http://localhost:8000`

## Option 2: Local Setup

If you prefer to run without Docker:

```bash
# 1. Install Python dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Install and start PostgreSQL
# (Installation varies by OS - see your OS docs)

# 3. Install and start Redis
# (Installation varies by OS - see your OS docs)

# 4. Set up environment
cp .env.example .env
# Edit .env with your database URLs and API keys

# 5. Initialize database
python -c "
import asyncio
from src.database import init_db
asyncio.run(init_db())
"

# 6. Start the application
uvicorn src.main:app --reload
```

## First Steps

### 1. Verify Installation

Visit the API documentation:
```
http://localhost:8000/docs
```

You should see the interactive Swagger UI with all available endpoints.

### 2. Run the Example

```bash
# Ensure the server is running
python examples/basic_usage.py
```

This example demonstrates:
- Creating an ad set
- Collecting metrics
- Predicting fatigue
- Generating creative variations
- Auto-rotating creatives

### 3. Create Your First Ad Set

Using curl:

```bash
curl -X POST http://localhost:8000/api/v1/ad-sets \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "my_first_adset",
    "platform": "meta",
    "name": "My First Campaign",
    "check_interval_minutes": 60,
    "auto_rotation_enabled": true
  }'
```

Using Python:

```python
import httpx
import asyncio

async def create_ad_set():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/ad-sets",
            json={
                "external_id": "my_first_adset",
                "platform": "meta",
                "name": "My First Campaign",
                "check_interval_minutes": 60,
                "auto_rotation_enabled": True
            }
        )
        print(response.json())

asyncio.run(create_ad_set())
```

### 4. Generate Creative Variations

First, create an original creative, then generate variations:

```bash
# Create original creative
curl -X POST http://localhost:8000/api/v1/creative/create \
  -H "Content-Type: application/json" \
  -d '{
    "ad_set_id": 1,
    "name": "Original Summer Sale Ad",
    "format": "image",
    "headline": "Get 50% Off Summer Collection",
    "body_text": "Shop now and save big on premium summer styles!",
    "call_to_action": "Shop Now"
  }'

# Generate variations (replace creative_id with the ID from above)
curl -X POST http://localhost:8000/api/v1/creative/generate \
  -H "Content-Type: application/json" \
  -d '{
    "original_creative_id": 1,
    "count": 5,
    "variation_types": ["hook", "angle", "copy"]
  }'
```

### 5. Monitor Fatigue

```bash
# Predict fatigue for an ad set
curl -X POST http://localhost:8000/api/v1/fatigue/predict \
  -H "Content-Type: application/json" \
  -d '{
    "ad_set_id": 1,
    "lookahead_days": 3
  }'

# Get current fatigue status
curl http://localhost:8000/api/v1/fatigue/status/1
```

### 6. Check Auto-Rotation

```bash
# Check if rotation is needed and execute if necessary
curl -X POST http://localhost:8000/api/v1/rotation/check/1
```

## Common Issues

### Database Connection Error

If you see "could not connect to server":

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# If using local PostgreSQL
pg_isready
```

### Redis Connection Error

```bash
# Check Redis is running
docker ps | grep redis

# If using local Redis
redis-cli ping
# Should return: PONG
```

### Import Errors

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all API endpoints at `/docs`
- Integrate with your ad platform (Meta, Google, etc.)
- Set up automated monitoring with background tasks
- Configure webhooks and notifications

## Production Deployment

For production deployment, see:
- Use proper secrets management (not .env files)
- Set up SSL/TLS
- Configure reverse proxy (nginx/traefik)
- Set up monitoring and logging
- Scale with multiple workers
- Use managed PostgreSQL and Redis

## Need Help?

- Check the [README.md](README.md)
- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue on GitHub
- Check `/docs` for API documentation

Happy optimizing! 🚀
