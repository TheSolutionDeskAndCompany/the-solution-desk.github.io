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
    { duration: '30s', target: 5 },   // Ramp up to 5 users
    { duration: '1m', target: 5 },    // Stay at 5 users for 1 minute
    { duration: '30s', target: 15 },  // Ramp up to 15 users
    { duration: '1m', target: 15 },   // Stay at 15 users for 1 minute
    { duration: '30s', target: 5 },   // Ramp down to 5 users
    { duration: '30s', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],  // 95% of requests should be below 300ms
    http_req_failed: ['rate<0.05'],    // Less than 5% of requests should fail
    errors: ['rate<0.05'],             // Less than 5% of operations should result in errors
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
  try {
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
  } catch (e) {
    console.error(`Request failed: ${e}`);
    errorRate.add(1);
    return null;
  }
  
  return response;
}

// Main test function
export default function () {
  // Test health check endpoint
  const healthRes = makeRequest('get', '/health');
  
  check(healthRes, {
    'health check successful': (r) => r && r.status === 200,
    'health status is ok': (r) => r && r.json('status') === 'ok',
  }) || errorRate.add(1);
  
  // Test API documentation endpoint
  const docsRes = makeRequest('get', '/docs');
  
  check(docsRes, {
    'docs endpoint accessible': (r) => r && r.status === 200,
    'docs content type is html': (r) => r && r.headers['Content-Type'].includes('text/html'),
  }) || errorRate.add(1);
  
  // Test registration
  const registerRes = makeRequest('post', '/auth/register', {
    email: TEST_USER,
    password: TEST_PASSWORD,
    name: 'Test User'
  });
  
  check(registerRes, {
    'registration successful': (r) => r && r.status === 201,
  }) || errorRate.add(1);
  
  // Test login
  const loginRes = makeRequest('post', '/auth/login', {
    email: TEST_USER,
    password: TEST_PASSWORD,
  });
  
  check(loginRes, {
    'login successful': (r) => r && r.status === 200,
    'received token': (r) => r && r.json('access_token') !== undefined,
  }) || errorRate.add(1);
  
  const token = loginRes ? loginRes.json('access_token') : null;
  
  // Test protected endpoint if login was successful
  if (token) {
    const protectedRes = makeRequest('get', '/auth/protected', null, token);
    
    check(protectedRes, {
      'protected endpoint accessible': (r) => r && r.status === 200,
      'correct user data': (r) => r && r.json('user.email') === TEST_USER,
    }) || errorRate.add(1);
    
    // Test invalid token
    const invalidTokenRes = makeRequest('get', '/auth/protected', null, 'invalid-token');
    
    check(invalidTokenRes, {
      'invalid token rejected': (r) => r && r.status === 401,
    }) || errorRate.add(1);
  }
  
  // Add a small sleep between iterations
  sleep(1);
}
