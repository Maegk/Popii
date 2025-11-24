## Contributing to Creative Fatigue Detection System

We welcome contributions! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd Popii
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start services**

```bash
docker-compose up -d
```

6. **Run the application**

```bash
uvicorn src.main:app --reload
```

## Code Style

- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Add docstrings to all classes and functions
- Run code formatters before committing:

```bash
# Format code
black src/
isort src/

# Check types
mypy src/

# Lint
flake8 src/
```

## Testing

Write tests for all new features:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_fatigue_detection.py
```

## Pull Request Process

1. **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new features
   - Update documentation as needed

3. **Run tests and linters**

```bash
pytest
black src/
flake8 src/
```

4. **Commit your changes**

```bash
git add .
git commit -m "feat: add your feature description"
```

Follow conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements

5. **Push and create PR**

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Project Structure

```
Popii/
├── src/
│   ├── api/              # API routes
│   ├── core/             # Core business logic
│   │   ├── monitoring.py # Metrics monitoring
│   │   ├── prediction.py # Fatigue prediction
│   │   ├── generation.py # Creative generation
│   │   ├── rotation.py   # Creative rotation
│   │   └── learning.py   # Learning engine
│   ├── models/           # Database models
│   ├── config.py         # Configuration
│   ├── database.py       # Database connection
│   ├── schemas.py        # Pydantic schemas
│   └── main.py           # FastAPI app
├── tests/                # Test suite
├── examples/             # Usage examples
├── config/               # Configuration files
└── docs/                 # Documentation
```

## Adding New Features

### 1. Add a New Prediction Model

Create a new predictor in `src/core/prediction.py`:

```python
class NewPredictor:
    def __init__(self, db_session):
        self.db = db_session

    async def predict(self, ad_set_id: int):
        # Your prediction logic
        pass
```

### 2. Add a New API Endpoint

Add to `src/main.py`:

```python
@app.get("/api/v1/your-endpoint")
async def your_endpoint(db: AsyncSession = Depends(get_db)):
    # Your logic
    return {"result": "data"}
```

### 3. Add a New Database Model

Create in `src/models/`:

```python
from src.models.base import Base, TimestampMixin

class YourModel(Base, TimestampMixin):
    __tablename__ = "your_table"
    # Define columns
```

Then create a migration:

```bash
alembic revision --autogenerate -m "Add your_table"
alembic upgrade head
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all new functions/classes
- Update API documentation if adding new endpoints
- Add examples in `examples/` for new features

## Questions?

Open an issue on GitHub or reach out to the maintainers.

Thank you for contributing! 🎉
