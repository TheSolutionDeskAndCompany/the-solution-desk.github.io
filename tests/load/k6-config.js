// k6 Configuration for different test scenarios
export const scenarios = {
  // Light load testing for CI
  ci: {
    stages: [
      { duration: '30s', target: 3 },
      { duration: '1m', target: 5 },
      { duration: '30s', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p(95)<3000'],
      http_req_failed: ['rate<0.1'],
    },
  },

  // Staging environment testing
  staging: {
    stages: [
      { duration: '1m', target: 5 },
      { duration: '3m', target: 10 },
      { duration: '2m', target: 15 },
      { duration: '3m', target: 15 },
      { duration: '1m', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p(95)<2000'],
      http_req_failed: ['rate<0.05'],
    },
  },

  // Production load testing
  production: {
    stages: [
      { duration: '2m', target: 10 },
      { duration: '5m', target: 20 },
      { duration: '3m', target: 30 },
      { duration: '5m', target: 30 },
      { duration: '3m', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p(95)<1500'],
      http_req_failed: ['rate<0.02'],
    },
  },

  // Stress testing
  stress: {
    stages: [
      { duration: '2m', target: 20 },
      { duration: '5m', target: 50 },
      { duration: '3m', target: 100 },
      { duration: '2m', target: 100 },
      { duration: '5m', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p(95)<5000'],
      http_req_failed: ['rate<0.1'],
    },
  },
};

// Environment-specific configurations
export const environments = {
  local: {
    apiUrl: 'http://localhost:5000',
    frontendUrl: 'http://localhost:3000',
  },
  staging: {
    apiUrl: 'https://ow-backend.onrender.com',
    frontendUrl: 'https://your-netlify-domain.netlify.app',
  },
  production: {
    apiUrl: 'https://api.thesolutiondesk.ca',
    frontendUrl: 'https://thesolutiondesk.ca',
  },
};
