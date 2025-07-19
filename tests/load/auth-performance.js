import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
export const errorRate = new Rate('errors');
export const authTrend = new Trend('auth_duration');
export const apiTrend = new Trend('api_duration');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 10 }, // Ramp up to 10 users over 2 minutes
    { duration: '5m', target: 10 }, // Stay at 10 users for 5 minutes
    { duration: '2m', target: 20 }, // Ramp up to 20 users over 2 minutes
    { duration: '5m', target: 20 }, // Stay at 20 users for 5 minutes
    { duration: '2m', target: 0 },  // Ramp down to 0 users over 2 minutes
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 2s
    http_req_failed: ['rate<0.05'],    // Error rate must be below 5%
    errors: ['rate<0.05'],             // Custom error rate below 5%
    auth_duration: ['p(95)<1500'],     // Auth endpoints below 1.5s
    api_duration: ['p(95)<1000'],      // API endpoints below 1s
  },
};

// Environment configuration
const BASE_URL = __ENV.API_URL || 'http://localhost:5000';
const FRONTEND_URL = __ENV.FRONTEND_URL || 'http://localhost:3000';

// Test data
const testUsers = [];
for (let i = 0; i < 50; i++) {
  testUsers.push({
    email: `loadtest${i}+${Date.now()}@example.com`,
    password: 'LoadTest123!',
  });
}

export function setup() {
  console.log(`🚀 Starting load test against: ${BASE_URL}`);
  console.log(`Frontend URL: ${FRONTEND_URL}`);
  
  // Health check
  const healthRes = http.get(`${BASE_URL}/health`);
  if (healthRes.status !== 200) {
    throw new Error(`Backend health check failed: ${healthRes.status}`);
  }
  
  return { baseUrl: BASE_URL, frontendUrl: FRONTEND_URL };
}

export default function (data) {
  const userIndex = __VU - 1; // VU index starts at 1
  const user = testUsers[userIndex % testUsers.length];
  
  // Test 1: User Registration
  testUserRegistration(user, data.baseUrl);
  sleep(1);
  
  // Test 2: User Login
  const token = testUserLogin(user, data.baseUrl);
  sleep(1);
  
  if (token) {
    // Test 3: Protected API calls
    testProtectedEndpoints(token, data.baseUrl);
    sleep(1);
    
    // Test 4: Token verification
    testTokenVerification(token, data.baseUrl);
    sleep(1);
  }
  
  // Random sleep between iterations
  sleep(Math.random() * 2 + 1);
}

function testUserRegistration(user, baseUrl) {
  const payload = JSON.stringify({
    email: user.email,
    password: user.password,
    confirmPassword: user.password,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const response = http.post(`${baseUrl}/api/auth/register`, payload, params);
  
  const success = check(response, {
    'registration status is 201': (r) => r.status === 201,
    'registration response has token': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.token && body.token.length > 0;
      } catch (e) {
        return false;
      }
    },
    'registration response time < 2s': (r) => r.timings.duration < 2000,
  });

  authTrend.add(response.timings.duration);
  errorRate.add(!success);

  if (!success) {
    console.error(`Registration failed for ${user.email}: ${response.status} ${response.body}`);
  }
}

function testUserLogin(user, baseUrl) {
  const payload = JSON.stringify({
    email: user.email,
    password: user.password,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const response = http.post(`${baseUrl}/api/auth/login`, payload, params);
  
  let token = null;
  const success = check(response, {
    'login status is 200': (r) => r.status === 200,
    'login response has token': (r) => {
      try {
        const body = JSON.parse(r.body);
        if (body.token && body.token.length > 0) {
          token = body.token;
          return true;
        }
        return false;
      } catch (e) {
        return false;
      }
    },
    'login response time < 1.5s': (r) => r.timings.duration < 1500,
  });

  authTrend.add(response.timings.duration);
  errorRate.add(!success);

  if (!success) {
    console.error(`Login failed for ${user.email}: ${response.status} ${response.body}`);
  }

  return token;
}

function testProtectedEndpoints(token, baseUrl) {
  const params = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  };

  // Test /api/auth/me endpoint
  const meResponse = http.get(`${baseUrl}/api/auth/me`, params);
  
  const success = check(meResponse, {
    'me endpoint status is 200': (r) => r.status === 200,
    'me endpoint has user data': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.user && body.user.email;
      } catch (e) {
        return false;
      }
    },
    'me endpoint response time < 1s': (r) => r.timings.duration < 1000,
  });

  apiTrend.add(meResponse.timings.duration);
  errorRate.add(!success);

  // Test token verification endpoint
  const verifyResponse = http.post(`${baseUrl}/api/auth/verify`, '{}', params);
  
  const verifySuccess = check(verifyResponse, {
    'verify endpoint status is 200': (r) => r.status === 200,
    'verify endpoint response time < 1s': (r) => r.timings.duration < 1000,
  });

  apiTrend.add(verifyResponse.timings.duration);
  errorRate.add(!verifySuccess);
}

function testTokenVerification(token, baseUrl) {
  const params = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  };

  const response = http.post(`${baseUrl}/api/auth/verify`, '{}', params);
  
  const success = check(response, {
    'token verification status is 200': (r) => r.status === 200,
    'token verification response time < 500ms': (r) => r.timings.duration < 500,
  });

  apiTrend.add(response.timings.duration);
  errorRate.add(!success);
}

export function teardown(data) {
  console.log('🏁 Load test completed');
  console.log(`Tested against: ${data.baseUrl}`);
}
