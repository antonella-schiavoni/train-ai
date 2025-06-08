# AI FastAPI Project

A modern FastAPI application for AI/ML services built with Poetry for dependency management.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **AI/ML Libraries**: PyTorch, Transformers, Scikit-learn, and more
- **Poetry**: Dependency management and packaging
- **Development Tools**: Black, isort, flake8, mypy for code quality
- **Testing**: Pytest with async support
- **Documentation**: Auto-generated API docs

## Quick Start

### Prerequisites

- Python 3.9+
- Poetry (installed automatically if not present)

### Installation

1. **Clone and setup the project:**
   ```bash
   git clone <your-repo-url>
   cd train-ai
   ```

2. **Install dependencies:**
   ```bash
   make install
   # or
   poetry install
   ```

3. **Run the development server:**
   ```bash
   make run
   # or
   poetry run uvicorn app.main:app --reload
   ```

4. **Visit the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Development

### Available Commands

Run `make help` to see all available commands:

```bash
make help              # Show available commands
make install           # Install dependencies  
make dev              # Install development dependencies
make test             # Run tests
make lint             # Run linting
make format           # Format code
make clean            # Clean cache files
make run              # Run development server
make deploy           # Deploy with gunicorn
make setup            # Initial project setup
```

### Project Structure

```
train-ai/
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── api/               # API routes
│   ├── core/              # Core functionality (config, logging)
│   ├── models/            # AI/ML models
│   ├── schemas/           # Pydantic models
│   └── services/          # Business logic services
├── tests/                 # Test files
├── pyproject.toml         # Poetry configuration
├── Makefile              # Development commands
└── README.md             # This file
```

### Adding Dependencies

**Production dependencies:**
```bash
poetry add package-name
```

**Development dependencies:**
```bash
poetry add --group dev package-name
```

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **mypy**: Type checking

Run all quality checks:
```bash
make lint
make format
```

### Testing

Run tests with:
```bash
make test
# or
poetry run pytest
```

## Deployment

### Development
```bash
make run
```

### Production
```bash
make deploy
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root:

```env
# API Settings
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Add your configuration variables here
```

## API Endpoints

- `GET /` - Root endpoint with basic info
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
