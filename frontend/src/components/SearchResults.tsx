import React from 'react';
import { AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { SearchResponse } from '../types/api';
import PaperCard from './PaperCard';

interface SearchResultsProps {
  results: SearchResponse | null;
  error: string | null;
  isLoading: boolean;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, error, isLoading }) => {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <span className="ml-4 text-gray-600">Searching across multiple sources...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <AlertCircle className="mx-auto h-12 w-12 text-red-500 mb-4" />
        <h3 className="text-lg font-medium text-red-800 mb-2">Search Error</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!results) {
    return null;
  }

  if (results.total_results === 0) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center">
        <AlertCircle className="mx-auto h-12 w-12 text-yellow-500 mb-4" />
        <h3 className="text-lg font-medium text-yellow-800 mb-2">No Results Found</h3>
        <p className="text-yellow-600 mb-4">
          No papers found for "{results.query}". Try different keywords or check your spelling.
        </p>
        <div className="text-sm text-yellow-600">
          <p>Tips:</p>
          <ul className="list-disc list-inside mt-2 space-y-1">
            <li>Use broader terms (e.g., "machine learning" instead of "deep neural networks")</li>
            <li>Try synonyms or alternative phrasings</li>
            <li>Check if all sources are enabled in advanced options</li>
          </ul>
        </div>
      </div>
    );
  }

  const getSourceStatus = (sourceName: string) => {
    const source = results.sources[sourceName];
    if (!source) return null;
    
    if (source.error) {
      return <XCircle className="w-4 h-4 text-red-500" />;
    }
    return <CheckCircle className="w-4 h-4 text-green-500" />;
  };

  return (
    <div className="space-y-6">
      {/* Results Summary */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Search Results for "{results.query}"
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">{results.total_results}</div>
            <div className="text-sm text-gray-600">Total Papers Found</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-700">
              {Object.keys(results.sources).length}
            </div>
            <div className="text-sm text-gray-600">Sources Searched</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-700">
              {results.search_params.sort_by}
            </div>
            <div className="text-sm text-gray-600">Sorted By</div>
          </div>
        </div>

        {/* Source Status */}
        <div className="border-t pt-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Source Status:</h3>
          <div className="flex flex-wrap gap-4">
            {Object.entries(results.sources).map(([sourceName, sourceData]) => (
              <div key={sourceName} className="flex items-center gap-2">
                {getSourceStatus(sourceName)}
                <span className="text-sm text-gray-600 capitalize">
                  {sourceName} ({sourceData.count} papers)
                </span>
                {sourceData.error && (
                  <span className="text-xs text-red-500">- Error</span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Papers */}
      <div className="space-y-6">
        {results.papers.map((paper) => (
          <PaperCard key={paper.id} paper={paper} />
        ))}
      </div>

      {/* Load More Hint */}
      {results.total_results >= results.search_params.max_results && (
        <div className="text-center py-6 text-gray-600">
          <p>Showing top {results.search_params.max_results} results.</p>
          <p className="text-sm">Increase max results in advanced options to see more.</p>
        </div>
      )}
    </div>
  );
};

export default SearchResults;
