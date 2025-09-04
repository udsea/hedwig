import axios from 'axios';
import { SearchRequest, SearchResponse } from '../types/api';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchPapers = async (searchRequest: SearchRequest): Promise<SearchResponse> => {
  const response = await api.post<SearchResponse>('/api/search/papers', searchRequest);
  return response.data;
};

export const healthCheck = async (): Promise<{ status: string; message: string }> => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
