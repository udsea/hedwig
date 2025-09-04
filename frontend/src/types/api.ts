// API types matching the backend models

export interface Author {
  name: string;
  affiliation?: string;
  orcid?: string;
}

export interface Paper {
  id: string;
  title: string;
  authors: Author[];
  abstract: string;
  source: string;
  source_name: string;
  published_date: string;
  url: string;
  doi?: string;
  categories?: string[];
  citation_count?: number;
  formatted_authors: string;
  primary_author: Author;
}

export interface SourceResult {
  papers: Paper[];
  count: number;
  error?: string;
}

export interface SearchResponse {
  query: string;
  total_results: number;
  papers: Paper[];
  sources: Record<string, SourceResult>;
  search_params: {
    max_results: number;
    sort_by: string;
    sources: string[];
  };
}

export interface SearchRequest {
  query: string;
  max_results?: number;
  sort_by?: 'relevance' | 'date' | 'citations';
  sources?: string[];
  date_from?: string;
  date_to?: string;
}

export type SortOption = 'relevance' | 'date' | 'citations';

export const SORT_OPTIONS: { value: SortOption; label: string }[] = [
  { value: 'relevance', label: 'Relevance' },
  { value: 'date', label: 'Date' },
  { value: 'citations', label: 'Citations' },
];

export const SOURCE_OPTIONS = [
  { value: 'arxiv', label: 'arXiv' },
  { value: 'openalex', label: 'OpenAlex' },
  { value: 'crossref', label: 'Crossref' },
];
