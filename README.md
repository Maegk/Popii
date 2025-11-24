# Automated Creative Fatigue Detection & Refresh System

An AI-powered system that automatically detects creative fatigue in advertising campaigns and generates fresh creative variations to maintain optimal performance.

## 🎯 What It Does

- **Real-time Monitoring**: Tracks frequency, CTR, CPA, and other key metrics across all ad sets
- **Predictive Detection**: Uses ML to detect fatigue BEFORE performance drops (not reactive)
- **AI Creative Generation**: Automatically generates creative variations (hooks, angles, formats)
- **Smart Rotation**: Auto-rotates creatives at optimal times based on predictive signals
- **Audience Learning**: Learns which creative elements work for specific audiences

## 📊 Why This Matters

- Creative quality accounts for **56% of Facebook ad performance**
- Seeing the same ad 6+ times can **drop purchase intent by 16%**
- Most brands need creative refresh every **7-14 days**
- Manual creative management is slow and reactive

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Ad Platforms (Meta, etc)                │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │      Metrics Collection          │
        │  (Frequency, CTR, CPA, etc)      │
        └────────────────┬────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │    Fatigue Detection Engine      │
        │    (ML-based prediction)         │
        └────────────────┬────────────────┘
                         │
                    [Fatigue?]
                         │
        ┌────────────────┴────────────────┐
        │   Creative Generation (AI)       │
        │  (New hooks, angles, formats)    │
        └────────────────┬────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │   Automated Rotation System      │
        │   (Deploy new creatives)         │
        └────────────────┬────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │      Learning Engine             │
        │  (Track what works per audience) │
        └──────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Meta Ads API access (optional for full integration)
- OpenAI or Anthropic API key (for creative generation)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Popii

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration

# Run database migrations
python -m alembic upgrade head

# Start the services
docker-compose up -d  # Start PostgreSQL and Redis

# Run the backend
uvicorn src.main:app --reload

# In a new terminal, start the frontend
cd frontend
npm install
npm run dev
```

The backend API will be available at `http://localhost:8000`
The frontend UI will be available at `http://localhost:3000`

### Configuration

Edit `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/creative_fatigue

# Redis
REDIS_URL=redis://localhost:6379/0

# Ad Platform APIs
META_ACCESS_TOKEN=your_meta_token
META_AD_ACCOUNT_ID=act_123456789

# AI APIs
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key

# Fatigue Detection Thresholds
FATIGUE_FREQUENCY_THRESHOLD=6
FATIGUE_CTR_DROP_PERCENT=20
FATIGUE_CPA_INCREASE_PERCENT=25
PREDICTION_LOOKAHEAD_DAYS=3
```

## 📖 Usage

### Web UI

The easiest way to use the system is through the modern web interface:

1. Start the backend: `uvicorn src.main:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. Open `http://localhost:3000` in your browser

**Features:**
- 📊 **Dashboard**: Real-time metrics, performance charts, fatigue distribution
- 🎯 **Ad Sets**: Manage and monitor all your ad sets
- ✨ **Creatives**: AI-powered creative generation and management
- ⚠️ **Fatigue Monitor**: Visual fatigue detection with radar charts and recommendations
- 📈 **Analytics**: Deep insights into creative performance
- ⚙️ **Settings**: Configure thresholds, API keys, and notifications

**Dark Mode**: Toggle between light and dark themes with the moon/sun icon

**Responsive**: Works on desktop, tablet, and mobile devices

### API Endpoints

```bash
# Start monitoring an ad set
curl -X POST http://localhost:8000/api/v1/monitor/ad-set \
  -H "Content-Type: application/json" \
  -d '{
    "ad_set_id": "123456789",
    "platform": "meta",
    "check_interval_minutes": 60
  }'

# Get fatigue status
curl http://localhost:8000/api/v1/fatigue/status/123456789

# Generate creative variations
curl -X POST http://localhost:8000/api/v1/creative/generate \
  -H "Content-Type: application/json" \
  -d '{
    "original_creative_id": "creative_123",
    "variations": 5,
    "variation_types": ["hook", "angle", "format"]
  }'

# Get performance insights
curl http://localhost:8000/api/v1/insights/ad-set/123456789
```

### Python SDK

```python
from src.core.monitoring import MetricsMonitor
from src.core.prediction import FatiguePredictor
from src.core.generation import CreativeGenerator

# Initialize monitor
monitor = MetricsMonitor(ad_set_id="123456789")
metrics = await monitor.get_current_metrics()

# Check for fatigue
predictor = FatiguePredictor()
fatigue_score = await predictor.predict_fatigue(ad_set_id="123456789")

if fatigue_score > 0.7:  # High fatigue risk
    # Generate new creatives
    generator = CreativeGenerator()
    variations = await generator.generate_variations(
        original_creative_id="creative_123",
        count=5
    )

    # Auto-deploy
    await generator.deploy_variations(variations)
```

## 🧠 How It Works

### 1. Metrics Monitoring

The system continuously monitors:
- **Frequency**: How many times each user sees the ad
- **CTR (Click-Through Rate)**: Percentage of impressions that result in clicks
- **CPA (Cost Per Action)**: Cost to acquire a customer
- **Engagement Rate**: Likes, comments, shares
- **Negative Feedback**: Hide/report actions

### 2. Fatigue Prediction

ML model analyzes:
- Historical performance trends
- Frequency distribution across audience
- Engagement decay patterns
- Time-series anomaly detection

**Prediction Algorithm**:
```python
fatigue_score = w1 * frequency_score
              + w2 * ctr_decay_score
              + w3 * cpa_increase_score
              + w4 * engagement_drop_score
```

### 3. Creative Generation

Uses AI (Claude/GPT) to generate variations:
- **Hook Variations**: Different opening lines/headlines
- **Angle Variations**: Different value propositions
- **Format Variations**: Image vs video, carousel vs single image
- **Copy Variations**: Different messaging styles

### 4. Smart Rotation

Rotates creatives based on:
- Fatigue prediction scores
- A/B test results
- Audience segment preferences
- Time of day/week patterns

### 5. Learning Engine

Continuously learns:
- Which creative elements work for which audiences
- Optimal rotation timing
- Creative lifespan patterns
- Combination effectiveness

## 📊 Dashboard Features

- Real-time fatigue scores for all ad sets
- Creative performance comparison
- Audience segment insights
- Automated rotation history
- ROI tracking

## 🔧 Advanced Configuration

### Custom Fatigue Rules

```python
# config/fatigue_rules.py
FATIGUE_RULES = {
    "frequency_threshold": 6,
    "ctr_drop_percent": 20,
    "cpa_increase_percent": 25,
    "min_impressions": 1000,
    "prediction_model": "gradient_boosting",
    "confidence_threshold": 0.7
}
```

### Creative Templates

```python
# config/creative_templates.py
TEMPLATES = {
    "hooks": [
        "Problem-Solution",
        "Question-Based",
        "Stat-Driven",
        "Story-Based"
    ],
    "formats": ["image", "video", "carousel", "collection"],
    "tones": ["professional", "casual", "urgent", "educational"]
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test suite
pytest tests/test_fatigue_detection.py
```

## 📈 Performance

- Monitors up to **10,000 ad sets** simultaneously
- Fatigue prediction latency: **< 100ms**
- Creative generation: **30-60 seconds** per variation
- Auto-rotation deployment: **< 5 minutes**

## 🛣️ Roadmap

- [ ] Multi-platform support (Google Ads, TikTok, LinkedIn)
- [ ] Advanced creative testing (multivariate)
- [ ] Budget optimization integration
- [ ] Mobile app for monitoring
- [ ] Webhook integrations
- [ ] Custom ML model training

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📧 Support

For issues and questions: [GitHub Issues](https://github.com/Maegk/Popii/issues)
