import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const stockDataService = {
  // 주식 데이터 가져오기
  getStockData: async () => {
    try {
      const response = await api.get('/api/stock-data');
      return response.data;
    } catch (error) {
      console.error('Error fetching stock data:', error);
      throw error;
    }
  },

  // 특정 키워드의 상세 보고서 생성
  generateReport: async (keyword, options = {}) => {
    try {
      const response = await api.post(`/api/reports/${keyword}`, {
        period: options.period || '24h',
        include_sentiment: options.include_sentiment !== false,
      });
      return response.data;
    } catch (error) {
      console.error('Error generating report:', error);
      throw error;
    }
  },

  // 키워드 히스토리 데이터 가져오기
  getHistory: async (keyword, days = 7) => {
    try {
      const response = await api.get(`/api/history/${keyword}`, {
        params: { days },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching history:', error);
      throw error;
    }
  },

  // 서버 상태 확인
  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking server health:', error);
      throw error;
    }
  },
};

export default api;