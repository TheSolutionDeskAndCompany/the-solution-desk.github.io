import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Configuration
const BASE_URL = __ENV.K6_PUBLIC_API_URL || 'http://localhost:5000';
const TEST_USER = `testuser_${Math.floor(Math.random() * 100000)}@example.com`;
const TEST_PASSWORD = 'testpass123';

// Custom metrics
const errorRate = new Rate('errors');

// Test options
export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up to 10 users
    { duration: '1m', target: 10 },   // Stay at 10 users for 1 minute
    { duration: '30s', target: 25 },  // Ramp up to 25 users
    { duration: '1m', target: 25 },   // Stay at 25 users for 1 minute
    { duration: '30s', target: 10 },  // Ramp down to 10 users
    { duration: '30s', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.1'],     // Less than 10% of requests should fail
    errors: ['rate<0.1'],              // Less than 10% of operations should result in errors
  },
};

// Helper function to handle API requests
function makeRequest(method, endpoint, payload = null, token = null) {
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  if (token) {
    params.headers['Authorization'] = `Bearer ${token}`;
  }
  
  let response;
  switch (method.toLowerCase()) {
    case 'get':
      response = http.get(`${BASE_URL}${endpoint}`, params);
      break;
    case 'post':
      response = http.post(`${BASE_URL}${endpoint}`, JSON.stringify(payload), params);
      break;
    default:
      throw new Error(`Unsupported HTTP method: ${method}`);
  }
  
  return response;
}

// Main test function
export default function () {
  // Test registration
  const registerRes = makeRequest('post', '/auth/register', {
    email: TEST_USER,
    password: TEST_PASSWORD,
    name: 'Test User'
  });
  
  check(registerRes, {
    'registration successful': (r) => r.status === 201,
  }) || errorRate.add(1);
  
  // Test login
  const loginRes = makeRequest('post', '/auth/login', {
    email: TEST_USER,
    password: TEST_PASSWORD,
  });
  
  check(loginRes, {
    'login successful': (r) => r.status === 200,
    'received token': (r) => r.json('access_token') !== undefined,
  }) || errorRate.add(1);
  
  const token = loginRes.json('access_token');
  
  // Test protected endpoint
  if (token) {
    const protectedRes = makeRequest('get', '/auth/protected', null, token);
    
    check(protectedRes, {
      'protected endpoint accessible': (r) => r.status === 200,
      'correct user data': (r) => r.json('user.email') === TEST_USER,
    }) || errorRate.add(1);
  }
  
  // Add a small sleep between iterations
  sleep(1);
}
