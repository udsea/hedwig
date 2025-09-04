import React, { useState } from 'react';
import { Search, Settings, X } from 'lucide-react';
import { SearchRequest, SortOption, SORT_OPTIONS, SOURCE_OPTIONS } from '../types/api';

interface SearchFormProps {
  onSearch: (searchRequest: SearchRequest) => void;
  isLoading: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [maxResults, setMaxResults] = useState(5);
  const [sortBy, setSortBy] = useState<SortOption>('relevance');
  const [selectedSources, setSelectedSources] = useState<string[]>(['arxiv', 'openalex', 'crossref']);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    onSearch({
      query: query.trim(),
      max_results: maxResults,
      sort_by: sortBy,
      sources: selectedSources.length > 0 ? selectedSources : undefined,
    });
  };

  const handleSourceToggle = (source: string) => {
    setSelectedSources(prev => 
      prev.includes(source) 
        ? prev.filter(s => s !== source)
        : [...prev, source]
    );
  };

  const exampleQueries = [
    "traffic flow optimization",
    "machine learning neural networks",
    "climate change modeling",
    "quantum computing algorithms",
    "sustainable energy systems"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Main Search Input */}
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your research problem (e.g., 'traffic networks', 'machine learning optimization')"
            className="search-input pr-12"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-primary-600 disabled:opacity-50"
          >
            <Search size={24} />
          </button>
        </div>

        {/* Advanced Options Toggle */}
        <div className="flex justify-between items-center">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800"
          >
            <Settings size={16} />
            {showAdvanced ? 'Hide' : 'Show'} Advanced Options
          </button>
          
          {!showAdvanced && (
            <div className="text-sm text-gray-500">
              Searching {selectedSources.length} source{selectedSources.length !== 1 ? 's' : ''}, 
              showing top {maxResults} results
            </div>
          )}
        </div>

        {/* Advanced Options */}
        {showAdvanced && (
          <div className="bg-gray-50 rounded-lg p-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Max Results */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Results
                </label>
                <select
                  value={maxResults}
                  onChange={(e) => setMaxResults(Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  {[5, 10, 15, 20].map(num => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>

              {/* Sort By */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort By
                </label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as SortOption)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  {SORT_OPTIONS.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Sources */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sources
              </label>
              <div className="flex flex-wrap gap-2">
                {SOURCE_OPTIONS.map(source => (
                  <button
                    key={source.value}
                    type="button"
                    onClick={() => handleSourceToggle(source.value)}
                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                      selectedSources.includes(source.value)
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    {source.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-center">
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="btn-primary text-lg px-8 py-3"
          >
            {isLoading ? 'Searching...' : 'Search Papers'}
          </button>
        </div>
      </form>

      {/* Example Queries */}
      {!query && (
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-600 mb-3">Try searching for:</p>
          <div className="flex flex-wrap justify-center gap-2">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                className="text-xs px-3 py-1 bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200 transition-colors"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchForm;
