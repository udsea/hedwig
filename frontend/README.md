# Hedwig Frontend

A modern React frontend for searching research papers, built with Vite, TypeScript, and Tailwind CSS.

## Features

- Clean, modern UI with Tailwind CSS
- Real-time paper search across multiple sources
- Advanced search filters (sources, sorting, result limits)
- Responsive design for all screen sizes
- TypeScript for type safety
- Fast development with Vite

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

## Installation

1. Install Bun (if not already installed):
```bash
curl -fsSL https://bun.sh/install | bash
```

2. Install dependencies:
```bash
cd frontend
bun install
```

## Development

Start the development server:
```bash
bun run dev
```

The app will be available at http://localhost:5173

## Build

Create a production build:
```bash
bun run build
```

Preview the production build:
```bash
bun run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   ├── services/        # API services
│   ├── types/          # TypeScript type definitions
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── index.css       # Global styles
├── public/             # Static assets
├── package.json        # Dependencies and scripts
└── README.md
```

## Components

- **SearchForm**: Main search interface with advanced options
- **SearchResults**: Display search results and status
- **PaperCard**: Individual paper display component

## API Integration

The frontend connects to the backend API at `http://localhost:8000`. Make sure the backend is running before using the frontend.

## Usage

1. Enter a research topic or problem in the search box
2. Optionally configure advanced options (sources, sorting, max results)
3. View results with paper details, authors, abstracts, and links
4. Click on paper titles or "Read Paper" links to access the full papers
