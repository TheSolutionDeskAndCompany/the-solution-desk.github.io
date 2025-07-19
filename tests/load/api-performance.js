import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
export const errorRate = new Rate('errors');
export const apiResponseTime = new Trend('api_response_time');

// Test configuration for API endpoints
export const options = {
  stages: [
    { duration: '1m', target: 5 },   // Ramp up to 5 users
    { duration: '3m', target: 15 },  // Ramp up to 15 users
    { duration: '3m', target: 15 },  // Stay at 15 users
    { duration: '1m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<1500'], // 95% of requests under 1.5s
    http_req_failed: ['rate<0.02'],    // Error rate under 2%
    errors: ['rate<0.02'],
    api_response_time: ['p(90)<1000'], // 90% of API calls under 1s
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:5000';

export function setup() {
  console.log(`🔧 Testing API performance against: ${BASE_URL}`);
  
  // Health check
  const healthRes = http.get(`${BASE_URL}/health`);
  if (healthRes.status !== 200) {
    throw new Error(`API health check failed: ${healthRes.status}`);
  }
  
  // Create a test user and get token for authenticated requests
  const registerPayload = JSON.stringify({
    email: `perftest+${Date.now()}@example.com`,
    password: 'PerfTest123!',
    confirmPassword: 'PerfTest123!',
  });

  const registerRes = http.post(`${BASE_URL}/api/auth/register`, registerPayload, {
    headers: { 'Content-Type': 'application/json' },
  });

  let token = null;
  if (registerRes.status === 201) {
    try {
      const body = JSON.parse(registerRes.body);
      token = body.token;
    } catch (e) {
      console.error('Failed to parse registration response');
    }
  }

  return { baseUrl: BASE_URL, token };
}

export default function (data) {
  // Test 1: Health endpoint (unauthenticated)
  testHealthEndpoint(data.baseUrl);
  sleep(0.5);

  // Test 2: Authentication endpoints
  testAuthEndpoints(data.baseUrl);
  sleep(0.5);

  if (data.token) {
    // Test 3: Protected endpoints
    testProtectedEndpoints(data.baseUrl, data.token);
    sleep(0.5);
  }

  // Random sleep between iterations
  sleep(Math.random() * 1 + 0.5);
}

function testHealthEndpoint(baseUrl) {
  const response = http.get(`${baseUrl}/health`);
  
  const success = check(response, {
    'health endpoint status is 200': (r) => r.status === 200,
    'health endpoint response time < 200ms': (r) => r.timings.duration < 200,
  });

  apiResponseTime.add(response.timings.duration);
  errorRate.add(!success);
}

function testAuthEndpoints(baseUrl) {
  // Test login with invalid credentials (should be fast)
  const loginPayload = JSON.stringify({
    email: 'invalid@example.com',
    password: 'wrongpassword',
  });

  const loginResponse = http.post(`${baseUrl}/api/auth/login`, loginPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  
  const loginSuccess = check(loginResponse, {
    'invalid login returns 401': (r) => r.status === 401,
    'login response time < 1s': (r) => r.timings.duration < 1000,
  });

  apiResponseTime.add(loginResponse.timings.duration);
  errorRate.add(!loginSuccess);
}

function testProtectedEndpoints(baseUrl, token) {
  const params = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  };

  // Test /api/auth/me
  const meResponse = http.get(`${baseUrl}/api/auth/me`, params);
  
  const meSuccess = check(meResponse, {
    'me endpoint status is 200': (r) => r.status === 200,
    'me endpoint response time < 800ms': (r) => r.timings.duration < 800,
  });

  apiResponseTime.add(meResponse.timings.duration);
  errorRate.add(!meSuccess);

  // Test /api/auth/verify
  const verifyResponse = http.post(`${baseUrl}/api/auth/verify`, '{}', params);
  
  const verifySuccess = check(verifyResponse, {
    'verify endpoint status is 200': (r) => r.status === 200,
    'verify endpoint response time < 500ms': (r) => r.timings.duration < 500,
  });

  apiResponseTime.add(verifyResponse.timings.duration);
  errorRate.add(!verifySuccess);
}

export function teardown(data) {
  console.log('🏁 API performance test completed');
}
