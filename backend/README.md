# Hedwig Backend

A research paper search API built with FastAPI using Domain-Driven Design (DDD) principles and SOLID design patterns.

## Features

- Search research papers across multiple sources:
  - arXiv
  - OpenAlex
  - Crossref
- RESTful API with FastAPI
- Clean architecture with DDD principles
- Async/await for concurrent API calls
- Comprehensive error handling

## Project Structure

```
backend/
├── src/
│   ├── domain/           # Domain layer (entities, value objects, repositories)
│   ├── application/      # Application layer (services, use cases)
│   ├── infrastructure/   # Infrastructure layer (API clients, external services)
│   ├── api/             # API layer (routes, models)
│   └── main.py          # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── README.md
```

## Installation

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
cd backend
python -m src.main
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Search Papers
- **POST** `/api/search/papers`
- **GET** `/api/search/papers`

Search for research papers based on a query string.

Example request:
```json
{
  "query": "traffic networks",
  "max_results": 5,
  "sort_by": "relevance",
  "sources": ["arxiv", "openalex", "crossref"]
}
```

### Health Check
- **GET** `/health`
- **GET** `/`

## Architecture

This project follows Domain-Driven Design (DDD) principles:

1. **Domain Layer**: Core business logic, entities, and repository interfaces
2. **Application Layer**: Use cases and application services
3. **Infrastructure Layer**: External API clients and data access implementations
4. **API Layer**: REST endpoints and request/response models

## SOLID Principles Applied

- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Extensible for new sources without modifying existing code
- **Liskov Substitution**: Repository implementations are interchangeable
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depends on abstractions, not concretions
