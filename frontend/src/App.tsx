import React, { useState } from 'react';
import { BookOpen } from 'lucide-react';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
import { searchPapers } from './services/api';
import { SearchRequest, SearchResponse } from './types/api';

function App() {
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (searchRequest: SearchRequest) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await searchPapers(searchRequest);
      setResults(response);
    } catch (err) {
      console.error('Search error:', err);
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred while searching for papers.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-center">
            <BookOpen className="h-8 w-8 text-primary-600 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">Hedwig</h1>
          </div>
          <p className="text-center text-gray-600 mt-2">
            Search for research papers across arXiv, OpenAlex, and Crossref
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Search Form */}
          <section>
            <SearchForm onSearch={handleSearch} isLoading={isLoading} />
          </section>

          {/* Results */}
          <section>
            <SearchResults 
              results={results} 
              error={error} 
              isLoading={isLoading} 
            />
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              Built with ❤️ using DDD principles and SOLID design patterns
            </p>
            <p className="text-sm">
              Data sources: arXiv, OpenAlex, and Crossref APIs
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
