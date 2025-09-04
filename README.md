# Hedwig - Research Paper Search Tool

     Built with clean architecture principles and modern web technologies.

## 🔍 What it does

Instead of just showing "top 5 papers," Hedwig allows you to search for papers related to specific research problems. For example:

- Search for "traffic networks" → Get papers about spatial-temporal analysis of traffic networks, traffic flow optimization, etc.
- Search for "machine learning optimization" → Get relevant ML optimization papers
- Search for "climate modeling" → Get climate science and modeling papers

## 🏗️ Architecture

### Backend (Python)
- **Domain-Driven Design (DDD)** with clean architecture
- **SOLID principles** throughout the codebase
- **FastAPI** for high-performance REST API
- **Async/await** for concurrent API calls to multiple sources
- **Repository pattern** for data access abstraction

### Frontend (React + Vite)
- **Modern React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for beautiful, responsive UI
- **Component-based architecture**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+ or Bun
- Git

### 1. Clone the repository
```bash
git clone <repository-url>
cd hedwig
```

### 2. Start the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

Backend will run at: http://localhost:8000

### 3. Start the Frontend
```bash
cd frontend
# Using Bun (recommended)
bun install
bun run dev

# Or using npm
npm install
npm run dev
```

Frontend will run at: http://localhost:5173

### 4. Use the Application
1. Open http://localhost:5173 in your browser
2. Enter a research problem (e.g., "traffic networks", "machine learning")
3. Optionally configure advanced options (sources, sorting, max results)
4. View and explore the results!

## 📁 Project Structure

```
hedwig/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── domain/         # Domain entities and business logic
│   │   ├── application/    # Application services and use cases
│   │   ├── infrastructure/ # External API clients
│   │   ├── api/           # REST API endpoints
│   │   └── main.py        # FastAPI app entry point
│   └── requirements.txt
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   ├── types/         # TypeScript types
│   │   └── App.tsx        # Main app component
│   └── package.json
└── README.md
```

## 🔧 Features

### Search Capabilities
- **Multi-source search**: arXiv, OpenAlex, Crossref
- **Intelligent querying**: Optimized search terms for each API
- **Concurrent requests**: Fast parallel API calls
- **Deduplication**: Removes duplicate papers across sources

### User Interface
- **Clean, modern design** with Tailwind CSS
- **Advanced search options**: Sort by relevance/date/citations
- **Source filtering**: Choose which databases to search
- **Responsive design**: Works on all screen sizes
- **Real-time search status**: See which sources are working

### Technical Features
- **Type safety**: Full TypeScript support
- **Error handling**: Graceful handling of API failures
- **Clean architecture**: Easy to extend and maintain
- **SOLID principles**: Well-structured, maintainable code

## 🎯 Example Searches

Try searching for these research problems:

- "traffic flow optimization"
- "machine learning neural networks"
- "climate change modeling"  
- "quantum computing algorithms"
- "sustainable energy systems"
- "natural language processing"
- "computer vision object detection"

## 🔄 API Endpoints

### Search Papers
- **POST** `/api/search/papers`
- **GET** `/api/search/papers`

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

## 🛠️ Development

### Backend Development
```bash
cd backend
source venv/bin/activate
python -m src.main  # Runs with auto-reload
```

### Frontend Development
```bash
cd frontend
bun run dev  # Hot reload enabled
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏛️ Architecture Principles

### Domain-Driven Design (DDD)
- **Domain Layer**: Core business entities (Paper, SearchQuery)
- **Application Layer**: Use cases and services
- **Infrastructure Layer**: External API integrations
- **API Layer**: REST endpoints and DTOs

### SOLID Principles
- **Single Responsibility**: Each class has one job
- **Open/Closed**: Easy to add new paper sources
- **Liskov Substitution**: Repository implementations are interchangeable
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depends on abstractions, not implementations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for your own research needs!

---

Built with ❤️ for researchers who need better paper discovery tools.
