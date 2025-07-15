// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import "@testing-library/jest-dom";

// Mock environment variables
process.env.REACT_APP_API_URL = 'http://localhost:5000';
process.env.REACT_APP_SENTRY_DSN = 'test-dsn';

// Suppress console errors during tests
const originalConsoleError = console.error;
console.error = (...args) => {
  // Ignore specific expected errors during testing
  if (args[0]?.includes('Error in the ErrorBoundary')) return;
  if (args[0]?.includes('Health-check failed')) return;
  originalConsoleError(...args);
};
