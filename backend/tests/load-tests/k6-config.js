// Configuration for k6 performance tests
export const config = {
  // CI configuration (used in GitHub Actions)
  ci: {
    vus: 5,
    duration: '1m',
    thresholds: {
      http_req_duration: ['p(95)<500'],
      http_req_failed: ['rate<0.1'],
    },
  },
  
  // Smoke test configuration (quick verification)
  smoke: {
    vus: 1,
    duration: '30s',
    thresholds: {
      http_req_duration: ['p(95)<1000'],
      http_req_failed: ['rate<0.1'],
    },
  },
  
  // Load test configuration (standard load)
  load: {
    stages: [
      { duration: '30s', target: 10 },
      { duration: '1m', target: 10 },
      { duration: '30s', target: 25 },
      { duration: '1m', target: 25 },
      { duration: '30s', target: 10 },
      { duration: '30s', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p(95)<500'],
      http_req_failed: ['rate<0.05'],
    },
  },
  
  // Stress test configuration (high load)
  stress: {
    stages: [
      { duration: '30s', target: 20 },
      { duration: '1m', target: 20 },
      { duration: '30s', target: 50 },
      { duration: '1m', target: 50 },
      { duration: '30s', target: 100 },
      { duration: '1m', target: 100 },
      { duration: '30s', target: 20 },
      { duration: '30s', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p(95)<1000'],
      http_req_failed: ['rate<0.1'],
    },
  },
};

// Get the current environment or default to 'load'
export function getConfig(env = __ENV.K6_ENV || 'load') {
  const configEnv = config[env] || config.load;
  return {
    ...configEnv,
    // Ensure we have standard k6 options
    vus: configEnv.vus || 1,
    duration: configEnv.duration || '30s',
    thresholds: {
      ...configEnv.thresholds,
      // Default thresholds if not specified
      http_req_duration: configEnv.thresholds?.http_req_duration || ['p(95)<500'],
      http_req_failed: configEnv.thresholds?.http_req_failed || ['rate<0.1'],
    },
  };
}
