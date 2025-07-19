/**
 * End-to-End Authentication Flow Tests
 * Tests the complete auth flow against staging environment
 */

describe('Authentication Flow E2E', () => {
  const generateTestUser = () => ({
    email: `test.user+${Date.now()}@example.com`,
    password: 'TestPass123!',
  });

  beforeEach(() => {
    // Clear localStorage before each test
    cy.clearLocalStorage();
    
    // Clear cookies
    cy.clearCookies();
    
    // Visit the app
    cy.visit('/');
  });

  describe('User Registration', () => {
    it('should register a new user successfully', () => {
      const user = generateTestUser();

      // Navigate to registration page
      cy.visit('/register');
      
      // Verify we're on the registration page
      cy.contains('Create Account').should('be.visible');
      
      // Fill out registration form
      cy.get('input[name="email"]').type(user.email);
      cy.get('input[name="password"]').type(user.password);
      cy.get('input[name="confirmPassword"]').type(user.password);
      
      // Submit registration
      cy.get('button[type="submit"]').click();
      
      // Should redirect to dashboard after successful registration
      cy.url().should('include', '/dashboard');
      
      // Should show success toast
      cy.contains('Registration successful!').should('be.visible');
      
      // Should have token in localStorage
      cy.window().then((window) => {
        const token = window.localStorage.getItem('token');
        expect(token).to.exist;
        expect(token).to.be.a('string');
        expect(token.length).to.be.greaterThan(0);
      });
    });

    it('should show error for duplicate email registration', () => {
      const user = generateTestUser();

      // Register user first time
      cy.visit('/register');
      cy.get('input[name="email"]').type(user.email);
      cy.get('input[name="password"]').type(user.password);
      cy.get('input[name="confirmPassword"]').type(user.password);
      cy.get('button[type="submit"]').click();
      
      // Wait for successful registration
      cy.url().should('include', '/dashboard');
      
      // Logout
      cy.contains('Logout').click();
      
      // Try to register with same email again
      cy.visit('/register');
      cy.get('input[name="email"]').type(user.email);
      cy.get('input[name="password"]').type(user.password);
      cy.get('input[name="confirmPassword"]').type(user.password);
      cy.get('button[type="submit"]').click();
      
      // Should show error message
      cy.contains('Email already registered').should('be.visible');
    });

    it('should validate password requirements', () => {
      const user = generateTestUser();

      cy.visit('/register');
      cy.get('input[name="email"]').type(user.email);
      
      // Test weak password
      cy.get('input[name="password"]').type('weak');
      cy.get('input[name="confirmPassword"]').type('weak');
      cy.get('button[type="submit"]').click();
      
      // Should show validation error
      cy.contains('Password must be at least 8 characters').should('be.visible');
    });
  });

  describe('User Login', () => {
    let testUser;

    beforeEach(() => {
      // Create a test user for login tests
      testUser = generateTestUser();
      
      // Register the user first
      cy.visit('/register');
      cy.get('input[name="email"]').type(testUser.email);
      cy.get('input[name="password"]').type(testUser.password);
      cy.get('input[name="confirmPassword"]').type(testUser.password);
      cy.get('button[type="submit"]').click();
      cy.url().should('include', '/dashboard');
      
      // Logout to prepare for login test
      cy.contains('Logout').click();
      cy.clearLocalStorage();
    });

    it('should login successfully with valid credentials', () => {
      cy.visit('/login');
      
      // Verify we're on login page
      cy.contains('Welcome Back').should('be.visible');
      
      // Fill out login form
      cy.get('input[name="email"]').type(testUser.email);
      cy.get('input[name="password"]').type(testUser.password);
      
      // Submit login
      cy.get('button[type="submit"]').click();
      
      // Should redirect to dashboard
      cy.url().should('include', '/dashboard');
      
      // Should show success toast
      cy.contains('Login successful!').should('be.visible');
      
      // Should have token in localStorage
      cy.window().then((window) => {
        const token = window.localStorage.getItem('token');
        expect(token).to.exist;
        expect(token).to.be.a('string');
      });
    });

    it('should show error for invalid credentials', () => {
      cy.visit('/login');
      
      // Try login with wrong password
      cy.get('input[name="email"]').type(testUser.email);
      cy.get('input[name="password"]').type('wrongpassword');
      cy.get('button[type="submit"]').click();
      
      // Should show error message
      cy.contains('Invalid email or password').should('be.visible');
      
      // Should not have token in localStorage
      cy.window().then((window) => {
        const token = window.localStorage.getItem('token');
        expect(token).to.be.null;
      });
    });
  });

  describe('Protected Routes & API Calls', () => {
    let testUser;

    beforeEach(() => {
      // Create and login test user
      testUser = generateTestUser();
      
      cy.visit('/register');
      cy.get('input[name="email"]').type(testUser.email);
      cy.get('input[name="password"]').type(testUser.password);
      cy.get('input[name="confirmPassword"]').type(testUser.password);
      cy.get('button[type="submit"]').click();
      cy.url().should('include', '/dashboard');
    });

    it('should access protected API endpoints with valid token', () => {
      // Get token from localStorage
      cy.window().then((window) => {
        const token = window.localStorage.getItem('token');
        
        // Test /api/auth/me endpoint
        cy.request({
          method: 'GET',
          url: `${Cypress.env('apiUrl')}/api/auth/me`,
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }).then((response) => {
          expect(response.status).to.eq(200);
          expect(response.body).to.have.property('user');
          expect(response.body.user).to.have.property('email', testUser.email);
        });
      });
    });

    it('should redirect to login when accessing protected routes without token', () => {
      // Clear token
      cy.clearLocalStorage();
      
      // Try to access protected route
      cy.visit('/dashboard');
      
      // Should redirect to login
      cy.url().should('include', '/login');
    });

    it('should handle token expiry gracefully', () => {
      // Set an expired token
      cy.window().then((window) => {
        const expiredToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDAwMDAwMDB9.invalid';
        window.localStorage.setItem('token', expiredToken);
      });
      
      // Try to access protected API
      cy.request({
        method: 'GET',
        url: `${Cypress.env('apiUrl')}/api/auth/me`,
        headers: {
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDAwMDAwMDB9.invalid'
        },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(401);
      });
    });
  });

  describe('Logout Functionality', () => {
    let testUser;

    beforeEach(() => {
      // Create and login test user
      testUser = generateTestUser();
      
      cy.visit('/register');
      cy.get('input[name="email"]').type(testUser.email);
      cy.get('input[name="password"]').type(testUser.password);
      cy.get('input[name="confirmPassword"]').type(testUser.password);
      cy.get('button[type="submit"]').click();
      cy.url().should('include', '/dashboard');
    });

    it('should logout successfully and clear token', () => {
      // Verify we have a token
      cy.window().then((window) => {
        const token = window.localStorage.getItem('token');
        expect(token).to.exist;
      });
      
      // Logout
      cy.contains('Logout').click();
      
      // Should show logout message
      cy.contains('You have been logged out').should('be.visible');
      
      // Token should be cleared
      cy.window().then((window) => {
        const token = window.localStorage.getItem('token');
        expect(token).to.be.null;
      });
      
      // Should redirect to home or login
      cy.url().should.not.include('/dashboard');
    });
  });

  describe('CORS and Network Configuration', () => {
    it('should not have CORS errors when making API calls', () => {
      const user = generateTestUser();

      // Register user and check for CORS errors
      cy.visit('/register');
      cy.get('input[name="email"]').type(user.email);
      cy.get('input[name="password"]').type(user.password);
      cy.get('input[name="confirmPassword"]').type(user.password);
      
      // Intercept the registration API call
      cy.intercept('POST', '**/api/auth/register').as('registerCall');
      
      cy.get('button[type="submit"]').click();
      
      // Wait for API call and verify no CORS errors
      cy.wait('@registerCall').then((interception) => {
        expect(interception.response.statusCode).to.be.oneOf([200, 201]);
        // Verify CORS headers are present (if needed)
        // expect(interception.response.headers).to.have.property('access-control-allow-origin');
      });
    });
  });
});
